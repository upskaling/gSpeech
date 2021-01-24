import os
import sys
from configparser import RawConfigParser, SafeConfigParser
from os.path import dirname, expanduser, isfile, join
from shutil import which

import gi

from .debug import is_debug_mode
from .i18n import (_comment, _developpers, _read_clipboard, _read_ocr,
                   _read_selected)


def ini_read(config_path, section, key, default):
    if isfile(config_path):
        parser = SafeConfigParser()
        parser.read(config_path)
        try:
            _property = parser.get(section, key)
        except Exception:
            _property = default
    else:
        _property = default
    if _property.lower() in ['1', 'yes', 'true', 'on']:
        return True
    if _property.lower() in ['0', 'no', 'false', 'off']:
        return False
    return _property


class Conf:
    app_name = 'gSpeech'
    # Temporaries files
    cache_path = join(os.getenv('HOME'), '.cache', app_name)

    developers = [
        ['Lahire Biette', '<tuxmouraille@gmail.com>'],
        ['Sardi Carlo', '<lusumdev@zoho.eu>'],
        ['Ferry Jérémie', '<jerem.ferry@gmail.com>'],
        ['upskaling', '<upskaling@42fr.net>']
    ]
    copyright_year = '2011, 2014, 2018, 2020, 2021'
    copyrights = 'Copyright © %s %s' % (
        copyright_year,
        ', '.join([name for name, mail in developers])
    )

    # Supported SVOX Pico's languages
    list_langs = ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT']

    list_source_languages = ['de-DE', 'en-GB',
                             'en-US', 'es-ES', 'fr-FR', 'it-IT']

    list_engine_trans = ['requests']
    if which('argos-translate-cli'):
        list_engine_trans.append('argos_translate')
    if which('trans'):
        list_engine_trans.append('translate_shell')

    list_synthesis_voice = ['pico']
    if which('espeak'):
        list_synthesis_voice.append('espeak')
    if which('spd-say'):
        list_synthesis_voice.append('spd-say')

    synthesis_voice = ''

    voice_speed = 1

    list_voice_speed = [0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2]

    list_option = [_read_clipboard, _read_selected]
    if which('tesseract'):
        list_option.append(_read_ocr)

    translators = [
        'Dupouy Paul (it-IT)',
        'Ferry Jérémie (fr-FR)'
    ]

    graphic_design = [
        'Baptiste Lhopitault'
    ]

    website = 'https://github.com/upskaling/gSpeech'

    show_notification = True
    has_app_indicator = True
    lang = ''
    source_languages = ''
    engine_trans = ''
    option = ''

    def set_dict(self, lang):
        self.dict_path = join(
            self.share_path,
            'gspeech/dict',
            lang.replace('-', '_')
        )
        if is_debug_mode():
            self.dict_path = join(
                self.dir,
                'dict',
                lang.replace('-', '_')
            )

    def set_lang(self, lang):
        if lang in self.list_langs:
            self.lang = lang
        if self.icons_dir:
            self.icon_path = join(
                self.icons_dir,
                self.app_name + '-' + lang + '.svg'
            )
        self.set_dict(lang)

    def set_source_languages(self, source_languages):
        if source_languages in self.list_source_languages:
            self.source_languages = source_languages

    def set_engine_trans(self, engine_trans):
        if engine_trans in self.list_engine_trans:
            self.engine_trans = engine_trans

    def set_speed(self, speed):
        if speed in self.list_voice_speed:
            self.voice_speed = speed

    def set_option(self, option):
        if option in self.list_option:
            self.option = option

    def set_synthesis_voice(self, synthesis_voice):
        if synthesis_voice in self.list_synthesis_voice:
            self.synthesis_voice = synthesis_voice

    def __init__(self, script_dir=None):
        self.pid = join(self.cache_path, 'gspeech.pid')
        self.temp_path = join(self.cache_path, 'speech.wav')

        self.dir = join(expanduser('~'), '.config/gSpeech')

        self.share_path = join(
            dirname(sys.modules['speech'].__file__),
            '..', '..', '..', '..', 'share'
        )
        self.local_dir = join(self.share_path, 'locale')
        self.icons_dir = join(
            self.share_path, 'icons/hicolor/scalable/apps'
        )
        if is_debug_mode():
            self.dir = join(dirname(dirname(__file__)))
            self.local_dir = join(self.dir, 'locale')
            self.icons_dir = join(self.dir, 'icons')
        
        self.icon_tran_path = join(
            self.icons_dir,
            self.app_name + '-trad.png'
        )

        self.path = join(self.dir, 'gspeech.conf')

        self.has_app_indicator = bool(ini_read(
            self.path, 'CONFIGURATION', 'USEAPPINDICATOR', 'True'
        ))

        lang = str(ini_read(
            self.path, 'CONFIGURATION', 'DEFAULTLANGUAGE', ''
        ))

        self.source_languages = str(ini_read(
            self.path, 'CONFIGURATION', 'DEFAULTLSOURCELANGUAGES', 'en-US'
        ))

        self.engine_trans = str(ini_read(
            self.path, 'CONFIGURATION', 'ENGINETRANS', 'requests'
        ))

        self.voice_speed = float(ini_read(
            self.path, 'CONFIGURATION', 'VOICESPEED', '1'
        ))

        self.synthesis_voice = str(ini_read(
            self.path, 'CONFIGURATION', 'SYNTHESISVOICE', 'pico'
        ))

        self.option = str(ini_read(
            self.path, 'CONFIGURATION', 'OPTION', ''
        ))

        self.show_notification = bool(ini_read(
            self.path,
            'CONFIGURATION',
            'SHOWNOTIFICATION',
            'True'
        ))
        self.lang = lang[:2] + '-' + lang[3:][:2]
        # if SVOX Pico not support this language, find os environment language
        if self.lang not in self.list_langs:
            self.lang = os.environ.get('LANG', 'en_US')[:2]
            self.lang += '-' + os.environ.get('LANG', 'en_US')[3:][:2]
            # if SVOX Pico not support this language, use US english
            if self.lang not in self.list_langs:
                self.lang = 'en-US'

        try:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3  # noqa: F401
            print('status : appindicator 3')
        except (ValueError, ImportError):
            self.has_app_indicator = False
            print('status : other')

        self.set_lang(self.lang)

        self.comment = _comment
        self.authors = '%s %s' % (
            _developpers,
            ', '.join([
                '%s (%s)' % (name, mail.replace('<', '').replace('>', ''))
                for name, mail in self.developers
            ]),
        )
        self.license = """
        Copyright © {0}
        {1}

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
        """.format(
            self.copyright_year,
            self.authors,
            self.app_name
        )

        if not isfile(self.path):
            self.update()

    def update(self):
        raw = RawConfigParser()
        raw.add_section('CONFIGURATION')
        raw.set(
            'CONFIGURATION',
            'USEAPPINDICATOR',
            self.has_app_indicator
        )
        raw.set(
            'CONFIGURATION',
            'DEFAULTLANGUAGE',
            self.lang
        )
        raw.set(
            'CONFIGURATION',
            'DEFAULTLSOURCELANGUAGES',
            self.source_languages
        )
        raw.set(
            'CONFIGURATION',
            'ENGINETRANS',
            self.engine_trans
        )
        raw.set(
            'CONFIGURATION',
            'VOICESPEED',
            self.voice_speed
        )
        raw.set(
            'CONFIGURATION',
            'SHOWNOTIFICATION',
            self.show_notification
        )
        raw.set(
            'CONFIGURATION',
            'SYNTHESISVOICE',
            self.synthesis_voice
        )
        raw.set(
            'CONFIGURATION',
            'OPTION',
            self.option
        )
        try:
            os.makedirs(self.dir, exist_ok=True)
            with open(self.path, 'w+') as stream:
                raw.write(stream)
        except Exception:
            return False
        return True
