import sys
import os
from os.path import join, dirname, abspath, isdir, isfile, expanduser
from configparser import RawConfigParser, SafeConfigParser

import gettext
import gi

def ini_read(config_path, section, key, default):
    if isfile(config_path):
        parser = SafeConfigParser()
        parser.read(config_path)
        try:
            _property = parser.get(section, key)
        except:
            _property = default
    else:
        _property = default
    if _property.lower() in ['1', 'yes', 'true', 'on'] :
        return True
    if _property.lower() in ['0', 'no', 'false', 'off'] :
        return False
    return _property


class Conf:
    app_name = "gSpeech"
    # Temporaries files
    cache_path = join(os.getenv('HOME'), '.cache', app_name)

    developers_name = "Lahire Biette, Sardi Carlo, Jérémie Ferry"
    authors_email = "<tuxmouraille@gmail.com>, <lusumdev@zoho.eu>, <jerem.ferry@gmail.com>"
    developers = developers_name + ' ' + authors_email
    copyright_year = '2011, 2014, 2018, 2020'
    copyrights = "Copyright © %s %s" % (copyright_year, developers_name)

    # Supported SVOX Pico's languages
    list_lang = ["de-DE", "en-GB", "en-US", "es-ES", "fr-FR", "it-IT"]

    translators = "pt-PT, pt-BR, es-ES &amp; it-IT :\n\
    Dupouy Paul"

    website = 'https://github.com/mothsart/gSpeech'

    show_notification = True
    use_appindicator = True
    lang = ''

    def setLang(self, lang):
        if lang in self.list_lang:
            self.lang = lang
        if self.icons_dir:
            self.icon_path = join(
                self.icons_dir,
                'icons',
                self.app_name + '-' + lang + '.svg'
            )

    def __init__(self, script_dir=None):
        self.pid = join(self.cache_path, 'gspeech.pid')
        self.temp_path = join(self.cache_path, 'speech.wav')

        self.dir = join(expanduser('~'), '.config/gSpeech')
        self.local_dir = '/usr/share/locale'
        self.icons_dir = '/usr/share/icons/hicolor/scalable/apps'
        if isdir('.git') and isdir('speech'):
            self.dir = join(dirname(dirname(__file__)))
            self.local_dir = join(self.dir, 'locale')
            self.icons_dir = self.dir

        self.path = join(self.dir, 'gspeech.conf')

        self.has_app_indicator = bool(ini_read(
            self.path, 'CONFIGURATION', 'USEAPPINDICATOR', 'True'
        ))
        lang = str(ini_read(
            self.path, 'CONFIGURATION', 'DEFAULTLANGUAGE', ''
        ))
        self.show_notification = bool(ini_read(self.path, 'CONFIGURATION', 'SHOWNOTIFICATION', 'True'))
        self.lang = lang[:2] + '-' + lang[3:][:2]
        # if SVOX Pico not support this language, find os environment language
        if not self.lang in self.list_lang:
            self.lang = os.environ.get('LANG', 'en_US')[:2] + '-' + os.environ.get('LANG', 'en_US')[3:][:2]
            # if SVOX Pico not support this language, use US english
            if not self.lang in self.list_lang:
                self.lang = "en-US"

        try:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3 as appindicator
        except:
            self.use_appindicator = False

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
        self.setLang(self.lang)
 
        gettext.install(self.app_name, self.local_dir)

        self.comment = _("A little script to read SVOX Pico texts selected with the mouse.")
        self.authors = [
            _("Developers :"),
            "%s" % (self.developers),
        ]
        self.license = """Copyright © {0} - {1}.

        {2} is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        {2} is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with {2}.  If not, see <http://www.gnu.org/licenses/>.
        """.format(self.copyright_year, self.authors, self.app_name)

        if not isfile(self.path):
            os.makedirs(self.dir, exist_ok = True)
            self.update()

    def update(self):
        raw = RawConfigParser()
        raw.add_section('CONFIGURATION')
        raw.set(
            'CONFIGURATION',
            'USEAPPINDICATOR',
            self.use_appindicator
        )
        raw.set(
            'CONFIGURATION',
            'DEFAULTLANGUAGE',
            self.lang
        )
        raw.set(
            'CONFIGURATION',
            'SHOWNOTIFICATION',
            self.show_notification
        )
        with open(self.path, 'w') as stream:
            raw.write(stream)
