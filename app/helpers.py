import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class IconMenuItem(Gtk.MenuItem):
    """Replaces Gtk.ImageMenuItem wich is deprecated"""
    def __init__(self, icon_name=None, label='', icon_size=5):
        super().__init__()
        label = Gtk.Label(label=label)
        box = Gtk.Box()
        self.add(box)
        if icon_name is not None:
            image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize(icon_size))
            box.pack_start(image, False, False, 0)
        box.pack_start(label, False, False, 0)
        self.show_all()
