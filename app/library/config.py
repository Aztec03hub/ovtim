import configparser
from localconfig import config
import app.main as app

def init():
    app.cfg = configparser.ConfigParser(interpolation=None)
    app.cfg.read("cfg.ini")
    
    # DEBUG Print a specific section
    #section = app.cfg['appLog']
    #for k in section:
    #    print('[appConfig] '+k+':', app.cfg['appLog'][k])
    
    # DEBUG Print entire config
    #for section_name, section in app.cfg.items():
    #    print("{:20s} - {} - {}".format(section_name, section, dict(section)))

    # Set configuration object with 'appLog' section as dictionary
    # Good practice to transform any integer vals from config to actual ints
    #app.cfg.appLog = dict(app.cfg.items('appLog'))
    #app.cfg.appLog['logrotatecount'] = int(app.cfg.appLog['logrotatecount'])
    #print('[appConfig] app.cfg.appLog:', app.cfg.appLog)

    # Set configuration object with 'bcLog' section as dictionary
    # Good practice to transform any integer vals from config to actual ints
    #app.cfg.bcLog = dict(app.cfg.items('bcLog'))
    #app.cfg.bcLog['logrotatecount'] = int(app.cfg.bcLog['logrotatecount'])
    #print('[appConfig] app.cfg.bcLog:', app.cfg.bcLog)

    # New Method, Set configuration objects with 'appLog' & 'bcLog' sections as dictionary
    config.read("cfg.ini")
    app.cfg.appLog = dict(list(config.applog))
    app.cfg.bcLog = dict(list(config.bclog))


    