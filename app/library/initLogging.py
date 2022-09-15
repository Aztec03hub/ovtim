import os
import logging
import logging.config
import logging.handlers

def init(cfg):
    #print('[initLogging] cfg:', cfg)

    # Check if logging path exists. If not, create it
    logPath = os.path.abspath(os.getcwd()) + '\logs' + cfg['path']
    #print('[initLogging] logPath:', logPath)
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    # Create Logger and set Log Level
    loggerName = cfg['filename'].split('.',1)[0]
    #print('[initLogging] loggerName:', loggerName)
    logger = logging.getLogger(loggerName)
    logger.setLevel(cfg['loglevel'])

    # Create Log Handler
    handler = logging.handlers.TimedRotatingFileHandler(
        filename = logPath + '/' + cfg['filename'],
        when = 'midnight',
        backupCount = cfg['logrotatecount']
    )

    # Create Log Formatter
    formatter = logging.Formatter(
        fmt = cfg['logmsgformat'],
        datefmt = cfg['logdateformat']
    )

    # Add Formatter to Handler
    handler.setFormatter(formatter)

    # Add Handler to Logger
    logger.addHandler(handler)

    # Output Initial Log Message
    logger.critical('Logging started for ' + loggerName)

    return logger


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
