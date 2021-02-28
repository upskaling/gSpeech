import os
import subprocess
import sys

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gst, Gtk

from .. import pid
from ..audioutils import (get_audio_commands, get_audio_commands_espeak,
                          run_audio_files)
from ..i18n import (_pause, _play, _read_clipboard, _read_ocr, _read_selected,
                    _trans_read)
from ..spd_say import spd_say, spd_say_cancel
from ..textutils import text_to_dict
from ..translate.main import translate
from ..widgets.ocr import ocr


def on_lang(ind, tray, lang, conf):
    """Action on language submenu items"""
    conf.set_lang(lang)
    conf.lang = lang
    conf.update()
    if conf.has_app_indicator:
        ind.set_icon(conf.icon_path)
        return
    tray.set_from_file(conf.icon_path)


def on_source_languages(lang, conf):
    conf.set_source_languages(lang)
    conf.source_languages = lang
    conf.update()


def on_engine_trans(engine_trans, conf):
    conf.set_engine_trans(engine_trans)
    conf.engine_trans = engine_trans
    conf.update()


def on_translate_url(url, conf):
    conf.set_translate_url(url)
    conf.translate_url = url
    conf.update()


def on_speed(speed, conf):
    """Action on voice speed submenu items"""
    conf.set_speed(float(speed))
    conf.voice_speed = float(speed)
    conf.update()


def on_option(option, conf):
    conf.set_option(option)
    conf.option = option
    conf.update()


def on_synthesis_voice(synthesis_voice, conf):
    conf.set_synthesis_voice(synthesis_voice)
    conf.synthesis_voice = synthesis_voice
    conf.update()


def on_reload(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    sources=None
):
    """Reload GUI"""
    myscript = os.path.abspath(sys.argv[0])
    subprocess.Popen(myscript)
    exit()


def on_media_dialog(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    sources=None
):
    """Show multimedia control dialog"""
    if window.get_property('visible'):
        window.hide()
        return
    window.show_all()


def on_destroy(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    sources=None
):
    """Destroy app on clicking Quit item"""
    if os.path.isfile(conf.temp_path):
        os.remove(conf.temp_path)
    pid.remove(conf.pid)
    Gtk.main_quit()


def changed_lang_menu(
    widget,
    ind,
    tray,
    lang,
    conf,
    lang_combobox,
    index=None
):
    on_lang(ind, tray, lang, conf)
    lang_combobox.active = index
    if widget.get_active():
        lang_combobox.set_active(index)


def changed_lang(lang_combobox, ind, tray, conf, menu_langs):
    model = lang_combobox.get_model()
    index = lang_combobox.get_active()
    if index is not None:
        on_lang(ind, tray, model[index][0], conf)
        menu_langs.get_children()[index].set_active(True)


def changed_engine_trans_menu(
    widget,
    engine_trans,
    conf,
    engine_trans_combobox,
    index=None
):
    on_engine_trans(engine_trans, conf)
    engine_trans_combobox.active = index
    if widget.get_active():
        engine_trans_combobox.set_active(index)


def changed_engine_trans(synthesis_voice_combobox, conf, menu_synthesis_voice):
    model = synthesis_voice_combobox.get_model()
    index = synthesis_voice_combobox.get_active()
    if index is not None:
        on_engine_trans(model[index][0], conf)
        menu_synthesis_voice.get_children()[index].set_active(True)


def changed_source_languages_menu(
    widget,
    source_languages,
    conf,
    source_languages_combobox,
    index=None
):
    on_source_languages(source_languages, conf)
    source_languages_combobox.active = index
    if widget.get_active():
        source_languages_combobox.set_active(index)


def changed_source_languages(
    source_languages_combobox,
    conf,
    menu_source_languages
):
    model = source_languages_combobox.get_model()
    index = source_languages_combobox.get_active()
    if index is not None:
        on_source_languages(model[index][0], conf)
        menu_source_languages.get_children()[index].set_active(True)


def changed_speed_menu(widget, speed, conf, speed_combobox, index=None):
    on_speed(speed, conf)
    speed_combobox.active = index
    if widget.get_active():
        speed_combobox.set_active(index)


def changed_speed(speed_combobox, conf, menu_voice_speed):
    model = speed_combobox.get_model()
    index = speed_combobox.get_active()
    if index is not None:
        on_speed(model[index][0], conf)
        menu_voice_speed.get_children()[index].set_active(True)


def changed_synthesis_voice_menu(widget, synthesis_voice, conf,
                                 synthesis_voice_combobox, index=None):
    on_synthesis_voice(synthesis_voice, conf)
    synthesis_voice_combobox.active = index
    if widget.get_active():
        synthesis_voice_combobox.set_active(index)


def changed_synthesis_voice(synthesis_voice_combobox,
                            conf, menu_synthesis_voice):
    model = synthesis_voice_combobox.get_model()
    index = synthesis_voice_combobox.get_active()
    if index is not None:
        on_synthesis_voice(model[index][0], conf)
        menu_synthesis_voice.get_children()[index].set_active(True)


def changed_option_menu(widget, option, conf, option_combobox, index=None):
    option_combobox.active = index
    on_option(option, conf)
    if widget.get_active():
        option_combobox.set_active(index)


def changed_option(option_combobox, conf, menu_option):
    model = option_combobox.get_model()
    index = option_combobox.get_active()
    if index is not None:
        on_option(model[index][0], conf)
        menu_option.get_children()[index].set_active(True)


def on_message(bus, message, player):
    """error message on playing function"""
    t = message.type
    if t == Gst.MessageType.EOS:
        # file ended, stop
        player.set_state(Gst.State.NULL)
    if t == Gst.MessageType.ERROR:
        # Error ocurred, print and stop
        player.set_state(Gst.State.NULL)
        err, debug = message.parse_error()
        print('Error: %s' % err, debug)


def on_left_click(
    widget,
    conf,
    menu_play_pause,
    win_play_pause,
    player
):
    """
    left click on status icon function
    function like this and not merge with on_execute
    to have possibility to use for something different
    """
    on_execute(widget, None, conf, menu_play_pause, win_play_pause, player)


def on_execute(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    sources=None
):
    """ execute text to speech"""

    if sources is None:
        sources = conf.source_languages

    if conf.option in _read_selected:
        text = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY).wait_for_text()
    elif conf.option in _read_clipboard:
        text = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()
    elif conf.option in _read_ocr:
        text = ocr(sources[:2])
    else:
        text = None

    if text is None:
        return

    conf.set_lang(conf.lang)

    if hasattr(widget, 'get_label') and _trans_read in widget.get_label():
        text = translate(
            text,
            sources=sources[:2],
            targets=conf.lang[:2],
            engine=conf.engine_trans,
            translate_url=conf.translate_url,
            key=conf.translate_key
        )

    if conf.synthesis_voice == "pico":
        text = text_to_dict(text, conf.dict_path, conf.lang)
        names, cmds = get_audio_commands(
            text,
            conf.temp_path,
            conf.lang,
            conf.cache_path,
            conf.voice_speed
        )
        run_audio_files(names, cmds, conf.temp_path)
        if player:
            player.set_state(Gst.State.NULL)
        player.set_state(Gst.State.PLAYING)
        button_state(menu_play_pause, win_play_pause, player)
    elif conf.synthesis_voice == "espeak":
        text = text_to_dict(text, conf.dict_path, conf.lang)
        names, cmds = get_audio_commands_espeak(
            text,
            conf.temp_path,
            conf.lang,
            conf.cache_path,
            conf.voice_speed
        )
        run_audio_files(names, cmds, conf.temp_path)
        if player:
            player.set_state(Gst.State.NULL)
        player.set_state(Gst.State.PLAYING)
        button_state(menu_play_pause, win_play_pause, player)
    elif conf.synthesis_voice == "spd-say":
        spd_say(text, conf.voice_speed)


def on_player(path):
    """Element playbin automatic plays any file"""
    player = Gst.ElementFactory.make('playbin', 'player')
    # Set the uri to the file
    player.set_property('uri', 'file://' + path)
    # Enable message bus to check for errors in the pipeline
    bus = player.get_bus()
    bus.add_signal_watch()
    bus.connect('message', on_message, player)
    return player


def on_play_pause(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    sources=None
):
    """play, pause and stop function for respectives items"""
    if (
        widget.get_label() == Gtk.STOCK_MEDIA_PLAY
        or (
            hasattr(widget, 'get_active')
            and not widget.get_active()
        )
    ):
        player.set_state(Gst.State.PLAYING)
    else:
        player.set_state(Gst.State.PAUSED)
    button_state(menu_play_pause, win_play_pause, player)


def on_stop(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    sources=None
):
    if conf.synthesis_voice == "pico":
        player.set_state(Gst.State.NULL)
        button_state(menu_play_pause, win_play_pause, player)
    elif conf.synthesis_voice == "espeak":
        player.set_state(Gst.State.NULL)
        button_state(menu_play_pause, win_play_pause, player)
    elif conf.synthesis_voice == "spd-say":
        spd_say_cancel()


def button_state(menu_play_pause, win_play_pause, player):
    gst_state = player.get_state(Gst.CLOCK_TIME_NONE)[1]
    if gst_state == Gst.State.PLAYING:
        win_play_pause.set_label(Gtk.STOCK_MEDIA_PAUSE)
        menu_play_pause.set_label(_pause)
        menu_play_pause.set_active(False)
        return
    win_play_pause.set_label(Gtk.STOCK_MEDIA_PLAY)
    menu_play_pause.set_label(_play)
    menu_play_pause.set_active(True)
