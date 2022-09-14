from telnetlib import Telnet
import threading
import socket

def tryTelnetConn(deviceIP, devicePort, testLAN, weblogger):
	try:
		tnclient = Telnet(str(deviceIP), int(devicePort), 5) #timeout is 5 seconds
		tnclient.close()
		testLAN[threading.current_thread().name] = 1
	except socket.timeout:
		pass
	except Exception as e:
		weblogger.debug('Scanner (' + str(deviceIP) + ':' + str(devicePort) + ') not connected via LAN- encountered error while connecting: ' + str(e))
		testLAN[threading.current_thread().name] = 0