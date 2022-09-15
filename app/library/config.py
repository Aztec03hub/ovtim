import configparser
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

    # Set configuration object with 'appLog' as dictionary
    app.cfg.appLog = dict(app.cfg.items('appLog'))
    #print('[appConfig] app.cfg.appLog:', app.cfg.appLog)

