import os
import codecs

def replace(text, dict_path):
    if not os.path.exists(dict_path):
        return text
    with codecs.open(dict_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            bad = line.split('=')[0]
            if line.find('=') == -1:
                continue
            good = line.split('=')[1].replace('\n', '')
            text = text.replace(bad, good)
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
