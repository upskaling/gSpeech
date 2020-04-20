import os, sys, tempfile, subprocess, multiprocessing
from configparser import SafeConfigParser

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init("")

from .conf import Conf
from . import pid
from .textutils import adaptTextToDict
from .audioutils import getAudioCommands
from .widgets.about import AboutDialog
from .widgets.save import SaveFileDialog
from .widgets import notify

try :
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
except :
    conf.has_app_indicator = False

#load configuration
conf = Conf()

class MainApp:
    ''' the main class of the software'''
    def __init__(self, conf):
        notify.init(conf)

        if conf.has_app_indicator == True:
            self.ind = appindicator.Indicator.new(
                conf.app_name,
                conf.icon_path,
                appindicator.IndicatorCategory.APPLICATION_STATUS
            )
            self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
            self.onRightClick(self, conf)
        else:
            self.tray = Gtk.StatusIcon()
            self.tray.set_from_file(conf.icon_path)
            self.tray.connect('popup-menu', self.onRightClick, conf)
            self.tray.connect('activate', self.onLeftClick, conf)
            self.tray.set_tooltip_text((_("SVOX Pico simple GUI")))

        self.window = Gtk.Dialog(
            conf.app_name,
            None,
            modal=True,
            destroy_with_parent=True
        )
        self.window.set_border_width(10)
        self.window.set_keep_above(True)
        self.window.set_icon_from_file(conf.icon_path)
        self.window.connect(
            'delete-event',
            lambda w, e: w.hide() or True
        )

        hbox = Gtk.HBox()

        # Create an accelerator group
        self.accelgroup = Gtk.AccelGroup()
        # Add the accelerator group to the toplevel window
        self.window.add_accel_group(self.accelgroup)

        button = Gtk.Button()
        button.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_EXECUTE,
            Gtk.IconSize.MENU
        ))
        button.set_label(_("Read clipboard content"))
        button.connect("clicked", self.onExecute, conf)
        button.add_accelerator(
            "clicked",
            self.accelgroup ,
            ord('c'),
            Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
        )
        hbox.pack_start(button, False, False, 0)

        button = Gtk.Button()
        button.set_image(
            Gtk.Image.new_from_stock(
                Gtk.STOCK_EXECUTE,
                Gtk.IconSize.MENU
            )
        )
        button.set_label(_("Read selected text"))
        button.connect("clicked", self.onExecute, conf)
        button.add_accelerator(
            "clicked",
            self.accelgroup ,
            ord('x'),
            Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
        )
        hbox.pack_start(button, False, False, 0)

        self.window.vbox.pack_start(hbox, False, False, 0)

        hbox = Gtk.HBox()

        self.WinPlayPause = Gtk.Button(stock = Gtk.STOCK_MEDIA_PAUSE)
        self.WinPlayPause.connect("clicked", self.onPlayPause)
        button.add_accelerator(
            "clicked",
            self.accelgroup ,
            ord('p'),
            Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
        )
        hbox.pack_start(self.WinPlayPause, False, False, 0)

        button = Gtk.Button(stock = Gtk.STOCK_MEDIA_STOP)
        button.connect("clicked", self.onStop)
        button.add_accelerator(
            "clicked",
            self.accelgroup,
            ord('q'),
            Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
        )
        hbox.pack_start(button, False, False, 0)

        button = Gtk.Button(stock = Gtk.STOCK_SAVE)
        button.connect("clicked", self.onSave, conf)
        button.add_accelerator(
            "clicked",
            self.accelgroup,
            ord('s'),
            Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
        )
        hbox.pack_end(button, False, False, 0)

        self.window.vbox.pack_start(hbox, False, False, 0)

        hbox = Gtk.HBox()

        combobox = Gtk.ComboBoxText.new()
        hbox.pack_start(combobox, False, False, 0)
        count = 0
        for i in conf.list_lang:
            combobox.append_text(i)
            if i == conf.lang:
                combobox.set_active(count)
            count += 1
        combobox.connect('changed', self.changed_cb)

        button = Gtk.Button(stock = Gtk.STOCK_CLOSE)
        button.connect_object("clicked", Gtk.Widget.hide, self.window)
        hbox.pack_end(button, False, False, 0)

        self.window.vbox.pack_start(hbox, False, False, 0)

    def changed_cb(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index:
            self.onLang(self, model[index][0], conf)
        return

    # action on right click
    def onRightClick(
        self,
        event_button=None,
        conf=None
    ):
        #print(icon, event_button, event_time, conf)
        # create menu
        menu = Gtk.Menu()

        # Execute menu item : execute speeching from Desktop clipboard
        rmItem = Gtk.MenuItem.new_with_label(_("Read clipboard content"))
        rmItem.connect('activate', self.onExecute, conf)
        rmItem.show()
        menu.append(rmItem)

        # Execute menu item : execute speeching from X.org clipboard
        rmItem = Gtk.MenuItem.new_with_label(_("Read selected text"))
        rmItem.connect('activate', self.onExecute, conf)
        rmItem.show()
        menu.append(rmItem)

        # Play item menu
        self.MenuPlayPause = Gtk.CheckMenuItem.new_with_label(_("Pause"))
        self.MenuPlayPause.set_active(False)
        self.MenuPlayPause.connect('toggled', self.onPlayPause)
        self.MenuPlayPause.show()
        menu.append(self.MenuPlayPause)

        # Stop  item menu
        rmItem = Gtk.MenuItem.new_with_label(_("Stop"))
        rmItem.connect('activate', self.onStop)
        rmItem.show()
        menu.append(rmItem)

        # Save item menu
        rmItem = Gtk.MenuItem.new_with_label(_("Save"))
        rmItem.connect('activate', self.onSave, conf)
        rmItem.show()
        menu.append(rmItem)

        # Separator
        rmItem =  Gtk.SeparatorMenuItem()
        rmItem.show()
        menu.append(rmItem)

        mediawin =  Gtk.MenuItem.new_with_label(_("Multimedia window"))
        mediawin.connect('activate', self.onMediaDialog)
        mediawin.show()
        menu.append(mediawin)

        # Separator
        rmItem =  Gtk.SeparatorMenuItem()
        rmItem.show()
        menu.append(rmItem)

        # Preference item menu
        rmItem = Gtk.MenuItem.new_with_label(_("Languages"))
        rmItem.show()
        # Creating and linking langues submenu
        menulngs = Gtk.Menu()
        rmItem.set_submenu(menulngs)

        # Creating languages items in submenu
        smItem = Gtk.RadioMenuItem()
        for i in conf.list_lang:
            smItem = Gtk.RadioMenuItem.new_with_label_from_widget(
                smItem,
                i
            )
            menulngs.append(smItem)
            smItem.connect("toggled", self.onLang, i, conf)
            if i == conf.lang:
                smItem.set_active(True)
            smItem.show()

        menu.append(rmItem)

        ## Reload item menu
        item = Gtk.MenuItem.new_with_label(_("Refresh"))
        item.connect('activate', self.onReload)
        item.show()
        menu.append(item)

        # About item menu : show About dialog
        about = Gtk.MenuItem.new_with_label(_("About"))
        about.connect('activate', self.onAbout, conf)
        about.show()
        menu.append(about)

        # Quit item menu
        item = Gtk.MenuItem.new_with_label(_("Quit"))
        item.connect('activate', self.destroy, conf)
        item.show()
        menu.append(item)

        if conf.has_app_indicator == True:
            menu.show()
            self.ind.set_menu(menu)
            return
        menu.popup(
            None,
            None,
            None,
            self.tray,
            event_button,
            event_time
        )

    def onReload(self, widget):
        '''Reload script'''
        myscript = os.path.abspath(sys.argv[0])
        subprocess.Popen(myscript)
        exit()

    def onLang(self, widget, lang, conf):
        '''Action on language submenu items'''
        conf.setLang(lang)
        conf.lang = lang
        if conf.has_app_indicator == True:
            self.ind.set_icon(conf.icon_path)
            return
        self.tray.set_from_file(conf.icon_path)

    def onAbout(self, widget, conf):
        '''Show about dialog'''
        self.aboutdiag = AboutDialog(conf)

    def onMediaDialog(self, widget):
        '''Show multimedia control dialog'''
        if self.window.get_property('visible'):
            self.window.hide()
            return
        self.window.show_all()

    # error message on playing function
    def onMessage(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            #file ended, stop
            self.player.set_state(Gst.State.NULL)
        if t == Gst.MessageType.ERROR:
            #Error ocurred, print and stop
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print( "Error: %s" % err, debug)

    # left click on status icon function
    # function like this and not merge with onExecute
    # to have possibility to use for something different
    def onLeftClick(self, widget, conf):
        self.onExecute(self, widget, conf)

    # on Execute item function : execute speech
    def onExecute(self, widget, conf):
        if widget.get_label() == _("Read selected text"):
            text = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY).wait_for_text()
        else:
            text = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()
        notify.get(conf, text)
        if text == None:
            return
        conf.setLang(conf.lang)
        text = adaptTextToDict(text, conf.dict_path, conf.lang)
        names, cmds = getAudioCommands(
            text,
            conf.temp_path,
            conf.lang,
            conf.cache_path
        )

        if len(cmds) == 1 :
            os.system(cmds[0])
        elif os.path.isfile('/usr/bin/sox'):
            nproc = int(.5 * multiprocessing.cpu_count())
            if nproc == 0:
                nproc = 1
            multiprocessing.Pool(nproc).map(os.system, cmds)
            os.system(
                'sox %s %s' % (
                    ' '.join(names),
                    conf.temp_path
                )
            )
            for fichier in names:
                os.remove(fichier)

        else:
            print("Le text est trop long pour être lue sans utiliser sox")
            exit()

        if hasattr(self, 'player'):
            self.player.set_state(Gst.State.NULL)
        player = self.onPlayer(conf.temp_path)
        self.player.set_state(Gst.State.PLAYING)
        self.buttonState()

    def onPlayer(self, path):
        #Element playbin automatic plays any file
        self.player = Gst.ElementFactory.make("playbin", "player")
        #Set the uri to the file
        self.player.set_property("uri", "file://" + path)
        #Enable message bus to check for errors in the pipeline
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.onMessage)

    # play, pause and stop function for respectivs items
    def onPlayPause(self, widget):
        if (
            widget.get_label() == Gtk.STOCK_MEDIA_PLAY
            or (
                hasattr(widget,'get_active')
                and widget.get_active() == False
            )
        ):
            self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.PAUSED)
        self.buttonState()

    def onStop(self, widget):
        self.player.set_state(Gst.State.NULL)
        self.buttonState()

    def buttonState(self):
        #block handler cause set_active activate the function onPlayPause
        self.MenuPlayPause.handler_block_by_func(self.onPlayPause)
        if Gst.State.PLAYING == self.player.get_state(Gst.CLOCK_TIME_NONE)[1]:
            self.WinPlayPause.set_label(Gtk.STOCK_MEDIA_PAUSE)
            self.MenuPlayPause.set_active(False)
        elif (
            Gst.State.PAUSED == self.player.get_state(Gst.CLOCK_TIME_NONE)[1]
            or Gst.State.NULL == self.player.get_state(Gst.CLOCK_TIME_NONE)[1]
        ):
            self.WinPlayPause.set_label(Gtk.STOCK_MEDIA_PLAY)
            self.MenuPlayPause.set_active(True)
        self.MenuPlayPause.handler_unblock_by_func(self.onPlayPause)

    def onSave(self, widget, conf):
        '''Saving file speech on clicking Save item'''
        SaveFileDialog(conf.temp_path)

    def destroy(self, widget, conf):
        '''Destroy app on clicking Quit item'''
        if os.path.isfile(conf.temp_path):
            os.remove(conf.temp_path)
        pid.remove(conf.pid)
        Gtk.main_quit()

    def main(self):
        Gtk.main()

def main():
    pid.kill_if_already_exist(conf.app_name, conf.pid)
    gSpeech = MainApp(conf)
    gSpeech.main()
