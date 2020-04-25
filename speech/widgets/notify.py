import gi
gi.require_version('Notify', '0.7')
from gi.repository.Notify import Notification
from gi.repository import Notify

def init(conf):
    Notify.init(conf.app_name)

def get(conf, text):
    if text == None:
        try:
            Notification.new(
                conf.app_name,
                _("No text selected."),
                conf.icon_path
            ).show()
        except:
            pass
        return
    try:
        Notification.new(
            conf.app_name,
            _("I'm reading the text. One moment please."),
            conf.icon_path
        ).show()
    except:
        pass
