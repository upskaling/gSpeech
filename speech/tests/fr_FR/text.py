from os.path import join, dirname

from unittest import TestCase

from speech.textutils import adaptTextToDict
from .data import datas


class TestTextConversion(TestCase):
    def test_text(self):
        for data in datas:
            text = data['ini']
            transform = data['new']
            lang = 'fr-FR'
            result = adaptTextToDict(
                text,
                join(
                    dirname(dirname(dirname(dirname(__file__)))),
                    'dict',
                    lang.replace('-', '_')
                ),
                lang
            )
            self.assertEqual(transform, result)
