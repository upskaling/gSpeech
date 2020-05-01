import gettext

import gi
from gi.repository import Gtk
gi.require_version('Gtk', '3.0')

_ = gettext.gettext


class OptionDialog(Gtk.Dialog):
    """ the options dialog class """

    def __init__(self, parent, conf):
        Gtk.Dialog.__init__(self, parent=parent)
        self.set_border_width(10)
        vbox = Gtk.VBox()
        box = self.get_content_area()
        box.add(vbox)
        hbox = Gtk.HBox()
        notification_check = Gtk.CheckButton(_('Active notification'))
        notification_check.set_active(conf.show_notification)
        notification_check.connect('toggled', self.on_checked, conf)
        hbox.add(notification_check)
        vbox.pack_start(hbox, False, False, 0)
        self.show_all()

    def on_checked(self, checkBox, conf):
        conf.show_notification = checkBox.get_active()
        conf.update()


def on_options(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """show options dialog"""
    OptionDialog(window, conf)
