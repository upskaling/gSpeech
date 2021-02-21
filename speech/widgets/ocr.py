from shutil import move, which
from subprocess import Popen, run
from tempfile import TemporaryDirectory


def screenshooter(screenshooter):

    if which('xfce4-screenshooter'):
        return ['xfce4-screenshooter', '--region', '--save', screenshooter]
    elif which('gnome-screenshot'):
        return ['gnome-screenshot', '--area', f'--file={screenshooter}']


def give_ocr_engine(screenshooter_image, temp_dir):
    screenshooter_out = f'{temp_dir}/screenshooter_out.png'

    if which('convert'):
        Popen(
            ['convert', '-colorspace', 'Gray', screenshooter_image,
                screenshooter_out]
        ).communicate()

        move(screenshooter_out, screenshooter_image)

    return screenshooter_image


def tesseract(lang, screenshooter_image, temp_dir):
    Popen(
        ['tesseract', '-l', lang,
         screenshooter_image, f'{temp_dir}/tesseract-out']
    ).communicate()

    with open(f'{temp_dir}/tesseract-out.txt', 'r') as target:
        text = target.read()

    return text


def cuneiform(lang, screenshooter_image, temp_dir):
    Popen(
        ['cuneiform', '-l', lang, '-o',
            f'{temp_dir}/cuneiform-out.txt', screenshooter_image]
    ).communicate()

    with open(f'{temp_dir}/cuneiform-out.txt', 'r') as target:
        text = target.read()

    return text


def ocr(lang='en'):
    temp_dir = TemporaryDirectory(suffix='_gSpeech')
    screenshooter_image = f'{temp_dir.name}/screenshooter.png'
    run(screenshooter(screenshooter_image), check=True)

    screenshooter_image = give_ocr_engine(screenshooter_image, temp_dir.name)

    lang_dit = {
        'de': 'ger',
        'en': 'eng',
        'es': 'spa',
        'fr': 'fra',
        'it': 'lit',
    }

    if which('tesseract'):
        return tesseract(lang_dit[lang], screenshooter_image, temp_dir.name)
    elif which('cuneiform'):
        return cuneiform(lang_dit[lang], screenshooter_image, temp_dir.name)
