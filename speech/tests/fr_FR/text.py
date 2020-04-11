from os.path import join, dirname

from unittest import TestCase

from speech.textutils import adaptTextToDict
from .data import datas


class TestTextConversion(TestCase):
    def test_text(self):
        for data in datas:
            text = data['init']
            transform = data['transform']
            lang = 'fr-FR'
            result = adaptTextToDict(
                text,
                join(dirname(dirname(dirname(dirname(__file__)))), 'dict', '%s.dic' % lang),
                lang
            )
            self.assertEqual(transform, result)
