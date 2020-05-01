import gettext

import gi
gi.require_version('Notify', '0.7')  # noqa E402
from gi.repository import Notify
from gi.repository.Notify import Notification

_ = gettext.gettext


def init(conf):
    Notify.init(conf.app_name)


def get(conf, text):
    if text is None:
        try:
            Notification.new(
                conf.app_name,
                _('No text selected.'),
                conf.icon_path
            ).show()
        except Exception:
            pass
        return
    try:
        Notification.new(
            conf.app_name,
            _("""I'm reading the text. One moment please."""),
            conf.icon_path
        ).show()
    except Exception:
        pass
