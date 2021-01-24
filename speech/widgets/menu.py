import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf

from ..i18n import (_about, _engine_trans, _languages, _menu_option,
                    _multimedia_window, _quit, _read, _refresh, _save,
                    _sources, _stop, _synthesis_voice, _trans_read,
                    _voice_speed, _preferences)
from .about import on_about
from .events import (changed_engine_trans_menu, changed_lang_menu,
                     changed_option_menu, changed_source_languages_menu,
                     changed_speed_menu, changed_synthesis_voice_menu,
                     on_destroy, on_execute, on_media_dialog, on_play_pause,
                     on_reload, on_stop)
from .save import on_save


def generic_item(
    menu,
    label,
    callback,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None,
    image=None
):
    """Generic item menu"""
    item = Gtk.MenuItem.new_with_label(label)
    if image:
        item = Gtk.ImageMenuItem.new_with_label(label)
        if "/" in image:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                image,
                width=20, height=20,
                preserve_aspect_ratio=False
            )
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            item.set_image(image)
        else:
            image = Gtk.Image.new_from_stock(
                image,
                Gtk.IconSize.MENU
            )
            item.set_image(image)
    item.connect(
        'activate',
        callback,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player,
    )
    menu.append(item)


def separator_item(menu):
    """Separator item"""
    item = Gtk.SeparatorMenuItem()
    menu.append(item)


def langs_item(menu, ind, tray, conf, lang_combobox, menu_langs):
    item = Gtk.MenuItem.new_with_label(_languages)
    item.show()
    item.set_submenu(menu_langs)
    # Creating languages items in submenu
    sub_item = Gtk.RadioMenuItem()
    for index, lang in enumerate(conf.list_langs):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            lang
        )
        menu_langs.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_lang_menu,
            ind,
            tray,
            lang,
            conf,
            lang_combobox,
            index
        )
        if lang == conf.lang:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def source_languages_item(menu, conf, source_languages_combobox, menu_langs):
    item = Gtk.MenuItem.new_with_label(_sources)
    item.show()
    item.set_submenu(menu_langs)

    sub_item = Gtk.RadioMenuItem()
    for index, source_languages in enumerate(conf.list_source_languages):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            source_languages
        )
        menu_langs.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_source_languages_menu,
            source_languages,
            conf,
            source_languages_combobox,
            index
        )
        if source_languages == conf.source_languages:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def engine_trans_item(menu, conf, engine_trans_combobox, menu_engine_trans):
    item = Gtk.MenuItem.new_with_label(_engine_trans)
    item.show()
    item.set_submenu(menu_engine_trans)

    sub_item = Gtk.RadioMenuItem()
    for index, engine_trans in enumerate(conf.list_engine_trans):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            engine_trans
        )
        menu_engine_trans.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_engine_trans_menu,
            engine_trans,
            conf,
            engine_trans_combobox,
            index
        )
        if engine_trans == conf.engine_trans:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def voice_speed_item(menu, conf, voice_combobox, menu_voice_speed):
    item = Gtk.MenuItem.new_with_label(_voice_speed)
    item.show()
    item.set_submenu(menu_voice_speed)
    # Creating voice speed items in submenu
    sub_item = Gtk.RadioMenuItem()
    for index, speed in enumerate(conf.list_voice_speed):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            str(speed)
        )
        menu_voice_speed.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_speed_menu,
            speed,
            conf,
            voice_combobox,
            index
        )
        if speed == conf.voice_speed:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def synthesis_voice_item(menu, conf, voice_combobox, menu_synthesis_voice):
    item = Gtk.MenuItem.new_with_label(_synthesis_voice)
    item.show()
    item.set_submenu(menu_synthesis_voice)

    sub_item = Gtk.RadioMenuItem()
    for index, synthesis_voice in enumerate(conf.list_synthesis_voice):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            str(synthesis_voice)
        )
        menu_synthesis_voice.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_synthesis_voice_menu,
            synthesis_voice,
            conf,
            voice_combobox,
            index
        )
        if synthesis_voice == conf.synthesis_voice:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def option_item(menu, conf, option_combobox, menu_option):
    item = Gtk.MenuItem.new_with_label(_menu_option)
    item.show()
    item.set_submenu(menu_option)

    sub_item = Gtk.RadioMenuItem()

    for index, option in enumerate(conf.list_option):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            str(option)
        )
        menu_option.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_option_menu,
            option,
            conf,
            option_combobox,
            index
        )
        if option == conf.option:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def on_right_click(
    icon,
    event_button,
    event_time,
    window,
    ind,
    tray,
    conf,
    menu_play_pause,
    win_play_pause,
    player,
    option_combobox,
    menu_option,
    lang_combobox,
    source_languages_combobox,
    menu_langs,
    menu_source_languages,
    engine_trans_combobox,
    menu_engine_trans,
    voice_combobox,
    menu_voice_speed,
    synthesis_voice_combobox,
    menu_synthesis_voice
):
    """action on right click : create menu"""
    menu = Gtk.Menu()
    generic_item(
        menu,
        _read,
        on_execute,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player,
        Gtk.STOCK_MEDIA_PLAY
    )
    generic_item(
        menu,
        _trans_read,
        on_execute,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player,
        conf.icon_tran_path
    )
    menu_play_pause.connect(
        'activate',
        on_play_pause,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player
    )
    menu.append(menu_play_pause)
    generic_item(
        menu,
        _stop,
        on_stop,
        menu_play_pause=menu_play_pause,
        win_play_pause=win_play_pause,
        player=player,
        image=Gtk.STOCK_MEDIA_STOP
    )
    generic_item(menu, _save, on_save, window, conf, image=Gtk.STOCK_SAVE)
    separator_item(menu)
    generic_item(menu, _multimedia_window, on_media_dialog, window)
    separator_item(menu)

    preferences = Gtk.Menu()
    item = Gtk.ImageMenuItem.new_with_label(_preferences)
    image = Gtk.Image.new_from_stock(
        Gtk.STOCK_PREFERENCES,
        Gtk.IconSize.MENU
    )
    item.set_image(image)
    item.set_submenu(preferences)
    option_item(preferences, conf, option_combobox, menu_option)
    langs_item(preferences, ind, tray, conf, lang_combobox, menu_langs)
    source_languages_item(
        preferences, conf, source_languages_combobox, menu_source_languages)
    engine_trans_item(preferences, conf, engine_trans_combobox, menu_engine_trans)
    voice_speed_item(preferences, conf, voice_combobox, menu_voice_speed)
    synthesis_voice_item(
        preferences, conf, synthesis_voice_combobox, menu_synthesis_voice)

    item.show()
    menu.append(item)

    generic_item(menu, _refresh, on_reload, image=Gtk.STOCK_REFRESH)
    generic_item(menu, _about, on_about, window, conf, image=Gtk.STOCK_ABOUT)
    generic_item(menu, _quit, on_destroy, conf=conf, image=Gtk.STOCK_QUIT)
    if conf.has_app_indicator:
        menu.show_all()
        ind.set_menu(menu)
        return
    menu.popup(
        None,
        None,
        None,
        tray,
        event_button,
        event_time
    )
