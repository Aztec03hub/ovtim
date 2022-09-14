import json
import ipaddress
import serial

# read and parse config file
# returns tuple: (returncode, dict containing all profiles, name of active profile, active profile has bottom side = 1 else 0, active profile has top side = 1 else 0)
# returncode values:
# 	0	no error
#	1	warning but all values could be parsed correctly (example no active profile)
#	2	error which prevents at least 1 profile from being parsed. (example no IP set) dictProfiles and activeprofiles will still return values
#	3	error which prevents the config file from being parsed (no profiles, both top and bottom sides have errors, etc)
def readConfig(weblogger, karlboxConfigFilePath, possibleIniValues, possibleModelValues):

	dictProfiles = {}
	returnCode = 0
	activeProfile = ''
	bottomEnabled = 0
	topEnabled = 0
	#returnTuple = ((returnCode, dictProfiles, activeProfile, bottomEnabled, topEnabled))

	karlboxConfig = json.load(open(karlboxConfigFilePath, 'r'))

	# check for existence of main section and if active profile is set
	try:
		if len(karlboxConfig['profiles']) <= 1:
			weblogger.error('Config file: no profiles saved or main section missing')
			returnCode = 3
			return ((returnCode, dictProfiles, activeProfile, bottomEnabled, topEnabled))
		if 'main' in karlboxConfig:
			if 'activeProfile' in karlboxConfig['main']:
				if len([x for x in karlboxConfig['profiles'] if x['profilename'] == karlboxConfig['main']['activeProfile']]) > 0:
					activeProfile = karlboxConfig['main']['activeProfile']
					weblogger.debug('Config file: active profile: ' + str(activeProfile))
				else:
					weblogger.warning('Config file: active profile not in config file')
					returnCode = 1
			else:
				weblogger.warning('Config file: active profile not set')
				returnCode = 1
		else:
			weblogger.error('Config file: error reading config- missing main section')
			returnCode = 3
			return ((returnCode, dictProfiles, activeProfile, bottomEnabled, topEnabled))
	except Exception as e:
		weblogger.error('Config file: error reading config- general exception reading sections: ' + str(e))
		returnCode = 3
		return ((returnCode, dictProfiles, activeProfile, bottomEnabled, topEnabled))
	
	# store all profiles
	for profile in karlboxConfig["profiles"]:
		profilename = profile['profilename']
		try:
			dictProfiles[profilename] = {}
			for key in possibleIniValues:
				if key in profile.keys():
					dictProfiles[profilename][key] = profile[key]
				else:
					dictProfiles[profilename][key] = ''
		except Exception as e:
			weblogger.error('Config file: general exception reading profile values: ' + str(e))
			returnCode = 2
			continue
 
		# check for existence of and validate values
		# bottom scanner
		dictProfiles[profilename]['bsenabled'] = 1
		if str(dictProfiles[profilename]['bscommtype']).lower() != 'rs232': # if commtype is not rs 232, it should be ethernet or "unknown" (default to ethernet)
			# check for valid IP
			dictProfiles[profilename]['bscommtype'] = 'ethernet'
			try:
				ip = ipaddress.ip_address(dictProfiles[profilename]['bsip'])
			except Exception as e:
				weblogger.warning('Config file: invalid bsip for ethernet commType: ' + str(dictProfiles[profilename]['bsip']) + ' (error msg): ' + str(e))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2

			# check for valid port
			try:
				port = int(dictProfiles[profilename]['bsport'])
				if 1 <= port <= 65535:
					pass
				else:
					raise Exception
			except Exception:
				weblogger.warning('Config file: invalid bsport for ethernet commType: ' + str(dictProfiles[profilename]['bsport']))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2
		else: # commtype is rs232
			# (attempt to) check for valid port
			try:
				if not str(dictProfiles[profilename]['bsport']).lower().startswith('com') and str(dictProfiles[profilename]['bsport']).lower().find('tty') == -1:
					# port doesnt start with com or contain tty in the value
					weblogger.warning('Config file: invalid bsport for serial commType: ' + str(dictProfiles[profilename]['bsport']))
					dictProfiles[profilename]['bsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid bsport for serial commType: ' + str(dictProfiles[profilename]['bsport']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2
			
			# check for valid baud rate
			try:
				if int(dictProfiles[profilename]['bsbaud']) not in serial.Serial.BAUDRATES:
					weblogger.warning('Config file: invalid bsbaud for serial commType: ' + str(dictProfiles[profilename]['bsbaud']))
					dictProfiles[profilename]['bsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid bsbaud for serial commType: ' + str(dictProfiles[profilename]['bsbaud']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2
			
			# check for valid byte size
			try:
				if int(dictProfiles[profilename]['bsbytesize']) not in serial.Serial.BYTESIZES:
					weblogger.warning('Config file: invalid bsbytesize for serial commType: ' + str(dictProfiles[profilename]['bsbytesize']))
					dictProfiles[profilename]['bsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid bsbytesize for serial commType: ' + str(dictProfiles[profilename]['bsbytesize']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2
			
			# check for valid stop bit
			try:
				if int(dictProfiles[profilename]['bsstopbit']) not in serial.Serial.STOPBITS:
					weblogger.warning('Config file: invalid bsstopbit for serial commType: ' + str(dictProfiles[profilename]['bsstopbit']))
					dictProfiles[profilename]['bsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid bsstopbit for serial commType: ' + str(dictProfiles[profilename]['bsstopbit']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2
			
			# check for valid parity
			try:
				if str(dictProfiles[profilename]['bsparity']) not in serial.Serial.PARITIES:
					weblogger.warning('Config file: invalid bsparity for serial commType: ' + str(dictProfiles[profilename]['bsparity']))
					dictProfiles[profilename]['bsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid bsparity for serial commType: ' + str(dictProfiles[profilename]['bsparity']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['bsenabled'] = 0
				returnCode = 2
		# check for valid model number
		try:
			if str(dictProfiles[profilename]['bsmodel']).lower() not in possibleModelValues:
				dictProfiles[profilename]['bsmodel'] = 'Other Scanner'
		except Exception:
			dictProfiles[profilename]['bsmodel'] = 'Other Scanner'

		# top scanner
		dictProfiles[profilename]['tsenabled'] = 1
		if str(dictProfiles[profilename]['tscommtype']).lower() != 'rs232':
			dictProfiles[profilename]['tscommtype'] = 'ethernet'
			# check for valid IP
			try:
				ip = ipaddress.ip_address(dictProfiles[profilename]['tsip'])
			except Exception as e:
				weblogger.warning('Config file: invalid tsip for ethernet commType: ' + str(dictProfiles[profilename]['tsip']) + ' (error msg): ' + str(e))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2

			# check for valid port
			try:
				port = int(dictProfiles[profilename]['tsport'])
				if 1 <= port <= 65535:
					pass
				else:
					raise Exception
			except Exception:
				weblogger.warning('Config file: invalid tsport for ethernet commType: ' + str(dictProfiles[profilename]['tsport']))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2
		else:
			# (attempt to) check for valid port
			try:
				if not str(dictProfiles[profilename]['tsport']).lower().startswith('com') and str(dictProfiles[profilename]['tsport']).lower().find('tty') == -1:
					# port doesnt start with com or contain tty in the value
					weblogger.warning('Config file: invalid tsport for serial commType: ' + str(dictProfiles[profilename]['tsport']))
					dictProfiles[profilename]['tsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid tsport for serial commType: ' + str(dictProfiles[profilename]['tsport']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2
			
			# check for valid baud rate
			try:
				if int(dictProfiles[profilename]['tsbaud']) not in serial.Serial.BAUDRATES:
					weblogger.warning('Config file: invalid tsbaud for serial commType: ' + str(dictProfiles[profilename]['tsbaud']))
					dictProfiles[profilename]['tsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid tsbaud for serial commType: ' + str(dictProfiles[profilename]['tsbaud']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2
			
			# check for valid byte size
			try:
				if int(dictProfiles[profilename]['tsbytesize']) not in serial.Serial.BYTESIZES:
					weblogger.warning('Config file: invalid tsbytesize for serial commType: ' + str(dictProfiles[profilename]['tsbytesize']))
					dictProfiles[profilename]['tsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid tsbytesize for serial commType: ' + str(dictProfiles[profilename]['tsbytesize']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2
			
			# check for valid stop bit
			try:
				if int(dictProfiles[profilename]['tsstopbit']) not in serial.Serial.STOPBITS:
					weblogger.warning('Config file: invalid tsstopbit for serial commType: ' + str(dictProfiles[profilename]['tsstopbit']))
					dictProfiles[profilename]['tsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid tsstopbit for serial commType: ' + str(dictProfiles[profilename]['tsstopbit']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2
			
			# check for valid parity
			try:
				if str(dictProfiles[profilename]['tsparity']) not in serial.Serial.PARITIES:
					weblogger.warning('Config file: invalid tsparity for serial commType: ' + str(dictProfiles[profilename]['tsparity']))
					dictProfiles[profilename]['tsenabled'] = 0
					returnCode = 2
			except Exception as e:
				weblogger.warning('Config file: invalid tsparity for serial commType: ' + str(dictProfiles[profilename]['tsparity']) + '(error msg): ' + str(e))
				dictProfiles[profilename]['tsenabled'] = 0
				returnCode = 2
		# check for valid model number
		try:
			if str(dictProfiles[profilename]['tsmodel']).lower() not in possibleModelValues:
				dictProfiles[profilename]['tsmodel'] = 'Other Scanner'
		except Exception:
			dictProfiles[profilename]['tsmodel'] = 'Other Scanner'
		# check if there is an active profile and if not, set it to first available profile that does not have errors
		if activeProfile == '':
			weblogger.debug('Config file: No active profile set; setting to first found valid profile: ' + str(profilename))
			activeProfile = profilename
		if profilename == activeProfile:
			bottomEnabled = dictProfiles[profilename]['bsenabled']
			topEnabled = dictProfiles[profilename]['tsenabled']
	return ((returnCode, dictProfiles, activeProfile, bottomEnabled, topEnabled))