#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import os

def replace(dict_path, text):
    if not os.path.exists(dict_path):
        return text
    for line in open(dict_path, 'r').readlines():
        bad = line.split('=')[0]
        if line.find('=') == -1:
            continue
        good = line.split('=')[1].replace('\n', '')
        text = text.replace(bad, good)
    return text

def adaptTextToDict( dict_path , text ):
    text = text.replace('\"', '')
    text = text.replace('`', '')
    text = text.replace('´', '')
    text = text.replace('-','')
    text = replace(dict_path, text)
    return text

