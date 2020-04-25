import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

from speech import __version__

class AboutDialog(Gtk.AboutDialog):
    """ the about dialog class """

    def __init__(self, parent, conf):
        Gtk.AboutDialog.__init__(self, parent = parent)
        self.set_logo(GdkPixbuf.Pixbuf.new_from_file(conf.icon_path))
        self.set_name(conf.app_name)
        self.set_version(__version__)
        self.set_copyright(conf.copyrights)
        self.set_license(conf.license)
        self.set_authors([mail for name, mail in conf.developers])
        self.set_comments(conf.comment)
        self.set_translator_credits('\n'.join(conf.translators))
        self.set_website(conf.website)
        self.set_website_label(_("%s's Website") % conf.app_name)
        self.connect("response", lambda self, *f: self.destroy())
        self.show_all()
