import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

from speech import __version__

class AboutDialog:
    """ the about dialog class """
    def __init__(self, conf):
        dialog = Gtk.AboutDialog()
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(conf.icon_path))
        dialog.set_name(conf.app_name)
        dialog.set_version(__version__)
        dialog.set_copyright(conf.copyrights)
        dialog.set_license(conf.license)
        dialog.set_authors(conf.authors)
        dialog.set_comments(conf.comment)
        dialog.set_translator_credits(conf.translators)
        dialog.set_website(conf.website)
        dialog.set_website_label(_("%s's Website") % conf.app_name)

        dialog.connect("response", lambda self, *f: self.destroy())
        dialog.show_all()
