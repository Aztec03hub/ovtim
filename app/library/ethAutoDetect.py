import threading
import time
import socket

def ethAutoDetect(side, testLAN, weblogger, socketio):
	devicesFound = {}
	broadcastIP = '192.168.188.255'
	
	def listenerHandler(listener):
		weblogger.debug('ScannerAutoDetect- Listener started')
		while testLAN[threading.current_thread().name] == 0:
			if time.time() - searchTimeoutTimer > 10:
				#app.logger.debug('ScannerAutoDetect- Timeout reached for finding new devices')
				return
			try:
				data, addr = listener.recvfrom(1024)
				deviceParameters = data.decode().split(',')
				if deviceParameters[6] != 'espip':
					devicesFound["deviceMac"] = deviceParameters[5]
					#if deviceMac not in devicesFound:
					devicesFound["deviceIP"] = deviceParameters[6]
					devicesFound["deviceTCP1"] = deviceParameters[14]
					devicesFound["deviceTCP2"] = deviceParameters[15]
					devicesFound["deviceUserName"] = deviceParameters[17]
					devicesFound["deviceModel"] = str(deviceParameters[19]).split('=')[1]
					devicesFound["deviceSerial"] = str(deviceParameters[22]).split('=')[1]
					devicesFound["deviceFirmware"] = str(deviceParameters[23]).split('=')[1]
					devicesFound["deviceWeblink"] = str(deviceParameters[24]).split('=')[1]
					weblogger.debug('ScannerAutoDetect- Found new device: deviceMac: {}, deviceIP: {}, deviceTCP1: {}, deviceTCP2: {}, deviceUserName: {}, deviceModel: {}, deviceSerial: {}, deviceFirmware: {}, deviceWeblink: {}'.format(devicesFound["deviceMac"], devicesFound["deviceIP"], devicesFound["deviceTCP1"], devicesFound["deviceTCP2"], devicesFound["deviceUserName"], devicesFound["deviceModel"], devicesFound["deviceSerial"], devicesFound["deviceFirmware"], devicesFound["deviceWeblink"]))
					testLAN[threading.current_thread().name] = 1
					return
					#devicesFound.append(deviceMac) # add to devices list
					#searchTimeoutTimer = time.time() # reset timer to continue scanning for other devices
				time.sleep(1)
			except Exception as e:
				weblogger.debug('ScannerAutoDetect- Thread ' + str(threading.current_thread().name) + ' encountered error while listening for broadcast message: ' + str(e))
				time.sleep(1)
				pass

	weblogger.info('ScannerAutoDetect- Trying to auto-detect compatible microhawk device connected via ethernet...')
	weblogger.debug('ScannerAutoDetect- Creating socket connections')
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	#server.settimeout(10)
	server.settimeout(0)
	listener.settimeout(0)

	weblogger.debug('ScannerAutoDetect- Binding sockets')
	listener.bind(("<broadcast>", 30717))
	server.bind(("", 30717))
	
	weblogger.debug('ScannerAutoDetect- Setting up listener thread')
	searchTimeoutTimer = time.time()
	t = threading.Thread(target=listenerHandler, args=(listener, ))
	t.setDaemon(True)
	testLAN[t.name] = 0
	t.start()

	startTimer = time.time()
	message = b"<op,019,00,FF:FF:FF:FF:FF:FF,255.255.255.255,espmac,espip,0,0>"
	server.sendto(message, (broadcastIP, 30717))
	weblogger.debug("ScannerAutoDetect- Broadcast message sent")
	attempts = 1
	while testLAN[t.name] == 0:
		if time.time() - startTimer > 5: # timeout 5 seconds
			if attempts > 2:
				weblogger.info('ScannerAutoDetect- Search finished, no compatible devices found')
				socketio.emit('Event_detectScannerInfoResult', {'result':'failure', 'side':side, 'ip':str(-1), 'tcp1':str(-1), 'name': '', 'model': '', 'mac':''})
				testLAN[t.name] = 0
				return
			else:
				attempts += 1
				startTimer = time.time()
				weblogger.debug('ScannerAutoDetect- No response in 5 seconds, resending broadcast (attempt ' + str(attempts) + ')')
				server.sendto(message, (broadcastIP, 30717))

	#app.logger.debug('ScannerAutoDetect- Search finished, found device')
	#app.logger.debug(devicesFound)
	if "deviceIP" in devicesFound.keys():
		weblogger.info('ScannerAutoDetect- Compatible Device Found: ' + str(devicesFound["deviceIP"]))
		socketio.emit('Event_detectScannerInfoResult', {'result':'success', 'side':side, 'ip':str(devicesFound["deviceIP"]), 'tcp1':str(devicesFound["deviceTCP1"]), 'name': str(devicesFound["deviceUserName"]), 'model': str(devicesFound["deviceModel"]), 'mac':str(devicesFound["deviceMac"])})
		return
	else:
		weblogger.info('ScannerAutoDetect- No compatible devices found')
		socketio.emit('Event_detectScannerInfoResult', {'result':'failure', 'side':side, 'ip':str(-1), 'tcp1':str(-1), 'name': '', 'model': '', 'mac':''})
		return