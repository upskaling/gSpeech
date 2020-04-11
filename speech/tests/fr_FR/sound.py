import os
from os.path import join, dirname
import shutil
import tempfile
from hashlib import md5
from unittest import TestCase

from speech.textutils import adaptTextToDict
from speech.audioutils import getAudioCommands

from .data import datas

assets_path = join(dirname(__file__), 'assets')
temp_path = tempfile.mkdtemp()

def create_sound(text, file_name):
    output_file = join(temp_path, '%s.wav' % file_name)
    lang = 'fr-FR'
    text = adaptTextToDict(
        text,
        join(dirname(dirname(dirname(dirname(__file__)))), 'dict', lang.replace('-', '_')),
        lang
    )
    names, cmds = getAudioCommands(
        text,
        output_file,
        lang,
        join(os.getenv('HOME'), '.cache', 'gSpeech')
    )
    os.system(cmds[0])

def md5_sum(path, file_name):
    with open(join(path, '%s.wav' % file_name), 'rb') as f:
        return md5(f.read()).hexdigest()

def tmp_sum(file_name):
    return md5_sum(temp_path, file_name)

def asset_sum(file_name):
    return md5_sum(assets_path, file_name)


class TestSound(TestCase):
    def __del__(self, *args, **kwargs):
        shutil.rmtree(temp_path)

    def test_sounds(self):
        for data in datas:
            text = data['ini']
            if 'file' not in data:
                continue
            file_name = data['file']
            create_sound(text, file_name)
            self.assertEqual(
                tmp_sum(file_name) + ' %s' % file_name,
                asset_sum(file_name) + ' %s' % file_name
            )
