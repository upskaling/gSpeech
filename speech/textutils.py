import os
import glob
import codecs

def _replacetxt(text, line):
    bad = line.split('=')[0]
    if line.find('=') == -1:
        return text
    good = line.split('=')[1].replace('\n', '')
    return text.replace(bad, good)

def replace(text, dict_path):
    if not os.path.isdir(dict_path):
        return text
    dict_list = glob.glob('%s/*dic' % dict_path)
    for path in sorted(dict_list):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                text = _replacetxt(text, line)
    return text

def adaptTextToDict(text, dict_path, lang):
    text = text.replace('\"', '')
    text = text.replace('`', '')
    text = text.replace('´', '')
    if lang != 'fr-FR':
        text = text.replace('-','')
    text = replace(text, dict_path)
    if lang == 'fr-FR':
        from .workers.fr_FR import acronyme
        text = acronyme.too_consonnant(text)
    return text.lower()
