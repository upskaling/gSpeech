from os.path import exists

def replace(dict_path, text):
    if not exists(dict_path):
        return text
    for line in open(dict_path, 'r').readlines():
        bad = line.split('=')[0]
        if line.find('=') == -1:
            continue
        good = line.split('=')[1].replace('\n', '')
        text = text.replace(bad, good)
    return text
