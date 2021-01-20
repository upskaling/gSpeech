import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
import argparse
import os
import socket
from sys import exit as sysexit
from sys import stderr

from gi.repository import Gdk, Gtk

from speech import __version__
from speech.audioutils import (get_audio_commands, get_audio_commands_espeak,
                               paplay, paplay_stop, run_audio_files)
from speech.conf import Conf
from speech.spd_say import spd_say
from speech.textutils import text_to_dict
from speech.translate.main import TransError, translate
from speech.widgets.ocr import ocr

conf = Conf()


def parse_arguments():
    '''
    parse arguments
    '''
    parser = argparse.ArgumentParser(
        description=f'{conf.app_name}'
        'is a small utility that allows you to read text.')
    parser.add_argument(
        '--selection',
        dest='selection',
        action='store_true',
        help='Since selection'
    )
    parser.add_argument(
        '--clipboard',
        dest='clipboard',
        action='store_true',
        help='From the clipboard'
    )
    parser.add_argument(
        '--ocr',
        dest='ocr',
        action='store_true',
        help='Optical Character Recognition'
    )
    parser.add_argument(
        '--stdin',
        dest='stdin',
        action='store_true',
        help="From the standard entrance"
    )
    parser.add_argument(
        '--input-file',
        dest='input_file',
        help='From a file'
    )
    parser.add_argument(
        '--input-text',
        dest='input_text',
        type=str,
        help='Text to read'
    )
    parser.add_argument(
        '-y',
        dest='synthesis_voice',
        choices=conf.list_synthesis_voice,
        default=conf.synthesis_voice,
        help=f"Set the synthesis voice default:{conf.synthesis_voice}")
    parser.add_argument(
        '-l', '--lang',
        dest='lang',
        nargs='?',
        const=conf.lang,
        choices=conf.list_langs,
        help="language")
    parser.add_argument(
        '-t', '--translation',
        dest='sources',
        nargs='?',
        const=conf.source_languages,
        choices=conf.list_source_languages,
        help=f"Language to source translation default:{conf.source_languages}")
    parser.add_argument(
        '--engine-trans',
        dest='engine_trans',
        nargs='?',
        const=conf.engine_trans,
        choices=conf.list_engine_trans,
        help=f"engine translation default:{conf.engine_trans}")
    parser.add_argument(
        '-s', '--speed',
        dest='speed',
        nargs='?',
        const=conf.voice_speed,
        type=float,
        choices=conf.list_voice_speed,
        help=f"Voice speed default:{conf.voice_speed}")
    parser.add_argument(
        '-o', '--output-file',
        dest='outfile',
        nargs='?',
        help="Name of the audio output file (wav type)")
    parser.add_argument(
        '-S', '--stop',
        dest='stop',
        action='store_true',
        help="stops playback")
    parser.add_argument(
        '-d', '--debug',
        dest='debug',
        action='store_true',
        help="debug mode")
    parser.add_argument(
        '-v', '--version',
        dest='version',
        action='store_true',
        help="show version information")
    return parser.parse_args()


def text_file(file_name):
    """Read text file"""
    if not os.path.isfile(file_name):
        print('Error: file not found')
        exit()
    with open(file_name, 'r') as f:
        return f.read()


class LockError(Exception):
    def __init__(self, message='[lock]'):
        super(LockError, self).__init__(message)


def get_lock(process_name):
    # https://stackoverflow.com/questions/788411/check-to-see-if-python-script-is-running/7758075#7758075

    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
    except OSError as erreur:
        raise LockError(erreur)


def main():
    args = parse_arguments()

    if args.version:
        print(f'{conf.app_name} version {__version__}')
        exit()

    if args.lang in conf.list_langs:
        conf.set_lang(args.lang)

    if args.sources in conf.list_voice_speed:
        conf.set_source_languages(args.sources)

    if args.engine_trans in conf.list_engine_trans:
        conf.set_engine_trans(args.engine_trans)

    if args.speed in conf.list_voice_speed:
        conf.set_speed(args.speed)

    if args.synthesis_voice in conf.synthesis_voice:
        conf.set_synthesis_voice(args.synthesis_voice)

    # conf.update()

    if args.stop:
        if args.synthesis_voice == "pico":
            paplay_stop()
        elif args.synthesis_voice == "espeak":
            paplay_stop()
        elif args.synthesis_voice == "spd-say":
            os.system('spd-say --cancel')
            os.system('killall spd-say')
        return

    try:
        get_lock(conf.app_name)
    except LockError as erreur:
        print(erreur, file=stderr)
        if args.synthesis_voice == "pico":
            paplay_stop()
        elif args.synthesis_voice == "espeak":
            paplay_stop()
        elif args.synthesis_voice == "spd-say":
            os.system('spd-say --cancel')

    if args.selection:
        text = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY).wait_for_text()
    elif args.clipboard:
        text = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()
    elif args.ocr:
        if args.sources:
            text = ocr(conf.lang[:2])
        else:
            text = ocr(conf.source_languages[:2])
    elif args.stdin:
        text = input()
    elif args.input_file:
        text = text_file(args.input_file)
    elif args.input_text:
        text = args.input_text
    else:
        return

    if args.speed in conf.list_voice_speed:
        conf.set_speed(args.speed)
    else:
        args.speed = conf.voice_speed

    outfile = conf.temp_path
    if args.outfile:
        outfile = args.outfile

    if args.sources:
        try:
            text = translate(
                text,
                sources=conf.source_languages[:2],
                targets=conf.lang[:2],
                config={'engine': conf.engine_trans})
        except TransError:
            sysexit(1)

    if args.synthesis_voice == "pico":
        text = text_to_dict(text, conf.dict_path, conf.lang, args.debug)
        names, cmds = get_audio_commands(
            text,
            outfile,
            conf.lang,
            conf.cache_path,
            args.speed
        )
        run_audio_files(names, cmds, outfile)
        if not args.outfile:
            paplay(outfile)
    elif conf.synthesis_voice == "espeak":
        names, cmds = get_audio_commands_espeak(
            text,
            outfile,
            conf.lang,
            conf.cache_path,
            conf.voice_speed
        )
        run_audio_files(names, cmds, outfile)
        if not args.outfile:
            paplay(outfile)
    elif args.synthesis_voice == "spd-say":
        spd_say(text, args.speed)
