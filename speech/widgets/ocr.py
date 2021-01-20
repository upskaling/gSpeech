from subprocess import DEVNULL, PIPE, Popen, run
from tempfile import TemporaryDirectory
from shutil import which


def screenshooter(screenshooter):

    if which('xfce4-screenshooter'):
        return ['xfce4-screenshooter', '--region', '--save', screenshooter]
    elif which('gnome-screenshot'):
        return ['gnome-screenshot', '--area', f'--file={screenshooter}']


def ocr(lang='fr'):
    lang_dit = {
        'fr': 'fra',
        'en': 'eng'
    }
    temp_dir = TemporaryDirectory(suffix='_gSpeech')
    screenshooter_image = f'{temp_dir.name}/screenshooter.png'
    run(screenshooter(screenshooter_image), check=True)

    tesseract = Popen(['tesseract', '-l', lang_dit[lang],
                       screenshooter_image, '-'],
                      stdout=PIPE,
                      stderr=DEVNULL)

    return tesseract.communicate()[0].decode()
