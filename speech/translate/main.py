from speech.audioutils import paplay

from .argos_translate import argos_translate
from .requests import translate_requests
from .translate_shell import trans


class TransError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


def translate(
    stdin,
    sources='en',
    targets='fr',
    config={"engine": 'requests',
            "translate_url": 'https://libretranslate.com/translate'}
):
    '''
    translate
    '''

    if len(stdin) >= 5000:
        return "5000 max caractère"

    paplay(outfile='/usr/share/sounds/freedesktop/stereo/device-added.oga')

    if config['engine'] == 'argos_translate':
        translate = argos_translate(stdin, sources, targets)
        stdout = translate.communicate()[0].decode()

    elif config['engine'] == 'requests':
        stdout = translate_requests(
            config['translate_url'], stdin, sources, targets)

    elif config['engine'] == 'translate_shell':
        translate = trans(sources=sources, targets=targets)
        stdout = translate.communicate(stdin.encode())[0].decode()

    else:
        paplay(
            outfile='/usr/share/sounds/freedesktop/stereo/device-removed.oga'
        )
        raise TransError("Could not be translated!")

    return stdout
