try:
    from configparser import RawConfigParser, SafeConfigParser
except:
    from ConfigParser import RawConfigParser, SafeConfigParser

import os

# Supported SVOX Pico's languages
LISTLANG = ["de-DE", "en-GB", "en-US", "es-ES", "fr-FR", "it-IT"]

def ini_read(configfile, section, key, default):
    if os.path.isfile(configfile):
        parser = SafeConfigParser()
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
    cache_path = os.path.join(os.getenv('HOME'), '.cache', app_name)

    def setLang(self,lang):
        if lang in LISTLANG:
            self.lang = lang
            self.dict_path = os.path.join(self.dir, '%s.dic' % self.lang)

    def __init__(self, script_dir=None):
        self.dir = os.path.join(os.path.expanduser('~'), '.config/gSpeech')
        if os.path.isdir('.git'):
            self.dir = './dict'

        if not os.path.isdir(self.dir):
            os.mkdir(self.dir, '0775')

        self.path = os.path.join(self.dir, 'gspeech.conf')
        if not os.path.isfile(self.path):
            config = RawConfigParser()
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
            self.lang = os.environ.get('LANG', 'en_US')[:2] + '-' + os.environ.get('LANG', 'en_US')[3:][:2]
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
        self.dict_path = os.path.join(self.dir, '%s.dic' % self.lang)
