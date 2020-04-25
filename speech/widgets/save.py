import os
import shutil

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SaveFileDialog(Gtk.FileChooserDialog):
    """ the class to save the speech .wav file """

    def __init__(self, parent, temp_path):
        Gtk.FileChooserDialog.__init__(
            self,
            _("Save the speech"),
            parent,
            Gtk.FileChooserAction.SAVE,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK
            )
        )
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_current_folder(os.path.expanduser('~'))

        _filter = Gtk.FileFilter()
        _filter.set_name(_("Wave file (*.wav)"))
        _filter.add_mime_type("audio/x-wav")
        _filter.add_pattern("*.wav")
        self.add_filter(_filter)

        response = self.run()
        if response == Gtk.ResponseType.OK:
            dest_path = dialog.get_filename() + '.wav'
            shutil.copy(temp_path, dest_path)