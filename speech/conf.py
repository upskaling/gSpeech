import sys
import os
from os.path import join, dirname, abspath, isdir
from configparser import RawConfigParser, SafeConfigParser

APPNAME = "gSpeech"

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
    if var.lower() in ['0', 'no', 'false', 'off'] :
        return False
    return var


class Conf:
    app_name = "gSpeech"
    # Temporaries files
    cache_path = os.path.join(os.getenv('HOME'), '.cache', app_name)

    def setLang(self, lang):
        if lang in LISTLANG:
            self.lang = lang

    def __init__(self, script_dir=None):
        self.dir = os.path.join(os.path.expanduser('~'), '.config/gSpeech')
        self.local_dir = '/usr/share/locale'
        self.icons_dir = '/usr/share/icons/hicolor/scalable/apps'
        if isdir('.git') and isdir('speech'):
            self.dir = join(dirname(dirname(__file__)))
            self.local_dir = join(self.dir, 'locale')
            self.icons_dir = abspath(dirname(sys.argv[0]))

        self.path = os.path.join(self.dir, 'gspeech.conf')
        if not os.path.isfile(self.path):
            os.makedirs(self.dir, exist_ok=True)
            config = RawConfigParser()
            config.add_section('CONFIGURATION')
            config.set('CONFIGURATION', 'USEAPPINDICATOR', 'True')
            config.set('CONFIGURATION', 'DEFAULTLANGUAGE', '')
            with open(self.path, 'w') as stream:
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

        self.dict_path = join(
            '/usr/share/gspeech/dict',
            self.lang.replace('-', '_')
        )
        if isdir('.git') and isdir('speech'):
            self.dict_path = join(
                self.dir,
                'dict',
                self.lang.replace('-', '_')
            )

        if self.icons_dir:
            #self.icon = join(self.icons_dir, 'icons', self.app_name + '.svg')
            self.icon = join(
                self.icons_dir,
                'icons',
                self.app_name + '-' + self.lang + '.svg'
            )
            print(self.icon)
