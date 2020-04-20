#!/usr/bin/env python3

import os
import glob
from setuptools import setup

from speech import __version__

I18NFILES = []
for filepath in glob.glob("locale/*/LC_MESSAGES/*.mo"):
    lang = filepath[len("locale/"):]
    targetpath = os.path.dirname(os.path.join("share/locale", lang))
    I18NFILES.append((targetpath, [filepath]))

setup(
    name='gspeech',
    version=__version__,
    description=(
        'A GUI for the Text To Speech Svoxpico.'
    ),
    author='mothsart',
    author_email='jerem.ferry@gmail.com',
    url='https://github.com/mothsart/gSpeech',
    packages=[ 'speech' ],
    data_files= I18NFILES,
    entry_points={
        'console_scripts': [
            'gspeech = gspeech:main'
        ]
    }
)
