import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
import argparse
import os
from sys import exit as sysexit

from gi.repository import Gdk, Gtk

from speech.audioutils import get_audio_commands, run_audio_files
from speech.conf import Conf
from speech.spd_say import spd_say
from speech.textutils import text_to_dict
from speech.translate.main import TransError, translate
from speech.widgets.ocr import ocr
from speech.widgets.paplay import paplay

conf = Conf()


def parse_arguments():
    '''
    parse arguments
    '''
    parser = argparse.ArgumentParser(
        description=f'{conf.app_name} is a small utility that allows you to read text.')
    parser.add_argument(
        '--selection',
        dest='selection',
        action='store_true',
        help='Depuis sélection'
    )
    parser.add_argument(
        '--clipboard',
        dest='clipboard',
        action='store_true',
        help='Depuis le presse-papier'
    )
    parser.add_argument(
        '--ocr',
        dest='ocr',
        action='store_true',
        help='Reconnaissance optique de caractères'
    )
    parser.add_argument(
        '--stdin',
        dest='stdin',
        action='store_true',
        help="Depuis l'entrée standard"
    )
    parser.add_argument(
        '--input-file',
        dest='input_file',
        help='Depuis un ficher'
    )
    parser.add_argument(
        '--input-text',
        dest='input_text',
        help='Depuis un ficher'
    )
    parser.add_argument(
        '-y',
        dest='synthesis_voice',
        choices=conf.list_synthesis_voice,
        default='pico',
        help="""Set the synthesis voice""")
    parser.add_argument(
        '-t', '--traduction',
        dest='sources',
        nargs='?',
        const='en-US',
        choices=conf.list_langs_trans,
        help="""traduction
                Langue sur source
                default:en-US""")
    parser.add_argument(
        '-s', '--speed',
        dest='speed',
        nargs='?',
        const='1',
        type=float,
        choices=conf.list_voice_speed,
        help="""voice speed""")
    parser.add_argument(
        '-o', '--output-file',
        dest='outfile',
        nargs='?',
        help="""name of the audio output file (wav type)""")
    parser.add_argument(
        '-S', '--stop',
        dest='stop',
        action='store_true',
        help="arrête la lecture")
    parser.add_argument(
        '-d', '--debug',
        dest='debug',
        action='store_true',
        help="debug mode")
    return parser.parse_args()


def text_file(file_name):
    """Read text file"""
    if not os.path.isfile(file_name):
        print('Error: file not found')
        exit()
    with open(file_name, 'r') as f:
        return f.read()


def main():
    args = parse_arguments()

    if args.selection:
        text = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY).wait_for_text()
    elif args.clipboard:
        text = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()
    elif args.ocr:
        print(args.sources)
        if args.sources:
            text = ocr(conf.lang)
        else:
            text = ocr(conf.lang_sources)
    elif args.stdin:
        text = input()
    elif args.input_file:
        text = text_file(args.input_file)
    elif args.input_text:
        text = args.input_text
    else:
        text = "error"

    if args.speed in conf.list_voice_speed:
        conf.set_speed(args.speed)
    else:
        args.speed = conf.voice_speed

    outfile = 'speech.wav'
    if args.outfile:
        outfile = args.outfile

    if args.sources:
        try:
            text = translate(
                text,
                sources=conf.lang_sources[:2],
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
    elif args.synthesis_voice == "spd-say":
        spd_say(text, args.speed)