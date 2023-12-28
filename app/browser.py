
import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from toolbox import (
    connection,
    debug_print,
    get_countries,
    )

from config import (
    BASE_DIR,
    __version__,
    )


class Browser(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Nord Manager browser")
        # icon
        icon_file = os.path.abspath(
            os.path.join(BASE_DIR, "icon_nordvpn_green.png"))
        self.set_default_icon_from_file(icon_file)
        # headerbar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.set_title("Nord Manager browser ({})".format(__version__))
        self.header_bar.set_subtitle('Choose a country or a city')
        self.set_titlebar(self.header_bar)
        # spinner
        self.spinner = Gtk.Spinner.new()
        self.header_bar.pack_end(self.spinner)
        self.spinner.start()

        # set the window
        self.set_properties(border_width=10)
        self.set_default_size(400, 500)
        self.set_size_request(300, 200)

        # scrolling window
        self.scroll = Gtk.ScrolledWindow()
        self.add(self.scroll)
        self.viewport = Gtk.Viewport()
        self.scroll.add(self.viewport)

        # get countries
        countries = get_countries()

        # boxes
        self.box = Gtk.VBox()
        self.viewport.add(self.box)

        for country in countries:
            box = Gtk.HBox()
            # gbox = Gtk.Grid()
            button = Gtk.Button(country['name'])
            debug_print(country['name'])
            # cities = reg(os.popen("nordvpn cities {}".format(country)))
            cities = country['cities']
            debug_print(cities)
            store = Gtk.ListStore(str)

            if len(cities) > 1:
                store.append(['-- Cities --'])
                for city in cities:
                    store.append([city])
                button2 = Gtk.ComboBox.new_with_model(store)
                # button2.set_title("-- Cities --")
                renderer_text = Gtk.CellRendererText()
                button2.pack_start(renderer_text, True)
                button2.add_attribute(renderer_text, "text", 0)
                button2.set_active(0)
                button2.connect("changed", self.combo_connecting)

            else:
                button2 = Gtk.Button(cities[0])
                button2.connect("clicked", self.connecting, cities[0])

            box.pack_start(button, True, True, 5)

            button.connect('clicked', self.connecting, country)
            box.pack_end(button2, True, True, 5)

            self.box.pack_start(box, False, False, 0)

    def combo_connecting(self, combo):
        iter = combo.get_active_iter()  # iter is a TreeIter object
        if iter is not None:
            model = combo.get_model()
            place = model[iter][0]
            if place != '-- Cities --':
                self.connecting(self, place)

    def connecting(self, source, place):
        connection(place)
        self.close()
