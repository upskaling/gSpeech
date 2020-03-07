try:
    import configparser
except:
    import ConfigParser

from os import getenv, environ
from os.path import join, isfile

from .debug import is_debug_mode

# Supported SVOX Pico's languages
LISTLANG = ["de-DE", "en-GB", "en-US", "es-ES", "fr-FR", "it-IT"]


def ini_read(configfile, section, key, default):
    if isfile(configfile):
        parser = ConfigParser.SafeConfigParser()
        parser.read(configfile)
        try:
            var = parser.get( section , key )
        except:
            var = default
    else:
        var = default

    if var.lower() in ['1', 'yes', 'true', 'on'] :
        return True
    elif var.lower() in ['0', 'no', 'false', 'off'] :
        return False
    else :
        return var


class Conf:
    app_name = "gSpeech"
    # Temporaries files
    cache_path = join(getenv('HOME'), '.cache', app_name)

    def __init__(self, script_dir=None):
        self.dir = '.'
        if is_debug_mode():
            print('DEBUG MODE')
        else:
            self.dir = join(expanduser('~'), '.config/gSpeech')
            if not os.path.isdir(conf.dir) :
                os.mkdir(conf.dir, 0775)

        self.path = join(self.dir, 'gspeech.conf')
        if not isfile(self.path):
            config = ConfigParser.RawConfigParser()
            config.add_section('CONFIGURATION')
            config.set('CONFIGURATION', 'USEAPPINDICATOR', 'True')
            config.set('CONFIGURATION', 'DEFAULTLANGUAGE', '')
            #~ config.set('CONFIGURATION', 'SHOWMEDIADIALOG', 'False')
            with open(self.path, 'wb') as stream:
                config.write(stream)

        self.has_app_indicator = bool(ini_read(
            self.path, 'CONFIGURATION', 'USEAPPINDICATOR', 'True' )
        )

        lang = str(ini_read(
            self.dir, 'CONFIGURATION', 'DEFAULTLANGUAGE', ''
        ))
        self.lang = lang[:2] + '-' + lang[3:][:2]
        # if SVOX Pico not support this language, find os environment language
        if not self.lang in LISTLANG:
            self.lang = environ.get('LANG', 'en_US')[:2] + '-' + environ.get('LANG', 'en_US')[3:][:2]
            # if SVOX Pico not support this language, use US english
            if not self.lang in LISTLANG:
                self.lang = "en-US"

        if script_dir:
            self.icon = join(script_dir, 'icons', self.app_name + '.svg')
            self.lang_icon = join(
                script_dir,
                'icons',
                self.app_name + '-' + self.lang + '.svg'
            )
        self.dict_path = join(self.dir, '%s.dic' % self.lang)
