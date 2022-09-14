import os
import logging
import logging.handlers

# initialize logging
# returns configured logger object
# Usage: app.logger = initLogging(app.instance_path, ovtimconfig.logConfigWebapp)
def initLogging(appInstancePath, configDict):
    # create log directory if it doesnt exist
    logDirectoryPath = os.path.join(
        appInstancePath, configDict['logdirectory'])
    if not os.path.isdir(logDirectoryPath):
        os.makedirs(logDirectoryPath, exist_ok=True)

    # initialize handler, formatter, and log level
    logFilepath = os.path.join(logDirectoryPath, configDict['basefilename'])
    configDict['loghandler'] = logging.handlers.TimedRotatingFileHandler(
        filename=logFilepath, when='midnight', backupCount=configDict['logrotatecount'])
    configDict['logformatter'] = logging.Formatter(
        configDict['logmsgformat'], datefmt=configDict['logdateformat'])
    configDict['loghandler'].setFormatter(configDict['logformatter'])
    logger = logging.getLogger(configDict['logname'])
    logger.addHandler(configDict['loghandler'])
    logger.setLevel(configDict['loglevel'])
    logger.critical('Logging started for ' + str(configDict['logname']))
    return logger
