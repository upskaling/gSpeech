import multiprocessing
import os
import subprocess
from shutil import which

import psutil

from .i18n import _text_to_long


def effect(text, speed=100, pitch=100, volume=120):
    _speed = '<speed level="%s">%s</speed>' % (speed, text)
    _pitch = '<pitch level="%s">%s</pitch>' % (pitch, _speed)
    return '<volume level="%s">%s</volume>' % (volume, _pitch)


def get_audio_commands(text, outfile, lang, cache_path, speed):
    overflow_len = 30000
    cmds = []
    names = []
    # low the limits to avoid overflow
    if len(text) <= overflow_len:
        cmds.append(
            ['pico2wave', '-l', lang, '-w', outfile, '--',
             effect(text, speed * 100)]
        )
        names.append(outfile)
        return names, cmds

    discours = text.split('.')
    text = ''
    for idx, paragraph in enumerate(discours):
        text += paragraph
        if (
            idx == len(discours) - 1
            # low the limits to avoid overflow
            or len(text) + len(discours[idx + 1]) >= overflow_len
        ):
            filename = cache_path + '/speech' + str(idx) + '.wav'
            cmds.append(
                ['pico2wave', '-l', lang, '-w', filename, '--',
                 effect(text, speed * 100)]
            )
            names.append(filename)
            text = ''
    return names, cmds


def get_audio_commands_espeak(
    text,
    outfile='out.wav',
    lang='fr-FR',
    cache_path='',
    speed=1,
    voice_tip=4
):
    speed = round((speed * 320) / 2)
    cmds = []
    names = []
    volume = 80
    pitch = round((speed * 45) / 320)
    voice = f'mb-{lang[:2]}{voice_tip}'
    cmds.append(
        ['espeak', '-v', voice, '-s', str(speed),
         '-p', str(pitch), '-a', str(volume), '-w', outfile, '--', text]
    )
    names.append(outfile)
    return names, cmds


def shell(cmd):
    return subprocess.call(cmd)


def run_audio_files(names, cmds, outfile='out.wav'):
    if len(cmds) == 1:
        subprocess.Popen(cmds[0]).communicate()
        return

    # rstrip is used to remove trailing spaces, that cause isfile function to
    # fail even if sox is present
    if not which('sox'):
        print(_text_to_long)
        return

    nproc = int(.5 * multiprocessing.cpu_count())
    if nproc == 0:
        nproc = 1

    multiprocessing.Pool(nproc).map(shell, cmds)

    subprocess.Popen(['sox'] + names + [outfile]).communicate()
    for _file in names:
        os.remove(_file)


def paplay(outfile, name='gspeech-cli'):
    return subprocess.Popen(['paplay', f'--client-name={name}', outfile])


def paplay_stop():
    for proc in psutil.process_iter():
        if '--client-name=gspeech-cli' in proc.cmdline():
            proc.kill()
