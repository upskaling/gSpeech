from speech.audioutils import paplay

from .argos_translate import argos_translate
from .libretranslate import translate_libretranslate
from .translate_shell import trans


class TransError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


def translate(
    stdin,
    sources='en',
    targets='fr',
    engine='requests',
    translate_url='https://libretranslate.com/translate',
    key='False'
):
    '''
    translate
    '''

    if len(stdin) >= 5000:
        return "5000 max caractère"

    paplay(outfile='/usr/share/sounds/freedesktop/stereo/device-added.oga')

    if engine == 'argos_translate':
        translate = argos_translate(stdin, sources, targets)
        stdout = translate.communicate()[0].decode()

    elif engine == 'libretranslate':
        stdout = translate_libretranslate(
            translate_url, stdin, sources, targets, key)

    elif engine == 'translate_shell':
        translate = trans(sources=sources, targets=targets)
        stdout = translate.communicate(stdin.encode())[0].decode()

    else:
        paplay(
            outfile='/usr/share/sounds/freedesktop/stereo/device-removed.oga'
        )
        raise TransError("Could not be translated!")

    return stdout
