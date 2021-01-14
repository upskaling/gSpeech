from subprocess import DEVNULL, PIPE, Popen, run
from tempfile import TemporaryDirectory
from shutil import which


def screenshooter(screenshooter):

    if which('xfce4-screenshooter'):
        return ['xfce4-screenshooter', '--region', '--save', screenshooter]
    # elif which('mate-screenshot'):
    #     return ['mate-screenshot', '--region', '--save', screenshooter]


def ocr(lang='fr'):
    lang_dit = {
        'fr': 'fra',
        'en': 'eng'
    }
    temp_dir = TemporaryDirectory(suffix='_screen-reader')
    run(screenshooter(f'{temp_dir.name}/screenshooter.png'), check=True)

    tesseract = Popen(['tesseract', '-l', lang_dit[lang], screenshooter, '-'],
                      stdout=PIPE,
                      stderr=DEVNULL)

    return tesseract.communicate()[0].decode()
