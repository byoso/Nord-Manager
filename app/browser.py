
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
    def __init__(self, countries: list):
        super().__init__(title="Nord Manager browser")
        # icon
        icon_file = os.path.abspath(
            os.path.join(BASE_DIR, "icon_nordvpn_green.png"))
        self.set_default_icon_from_file(icon_file)
        self.set_position(Gtk.WindowPosition.CENTER)
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
        self.set_size_request(600, 600)

        # scrolling window
        self.scroll = Gtk.ScrolledWindow()
        self.add(self.scroll)
        self.viewport = Gtk.Viewport()
        self.scroll.add(self.viewport)

        # boxes
        self.box = Gtk.VBox()
        self.viewport.add(self.box)

        for country in countries:
            button = Gtk.Button(country['name'])
            debug_print(country['name'])
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
                button2.connect("clicked", self.connecting, cities[0].lower().replace(" ", "_"))

            button.connect('clicked', self.connecting, country['name'].lower().replace(" ", "_"))

            grid = Gtk.Grid()
            grid.set_column_spacing(10)
            grid.attach(button, 0, countries.index(country), 30, 1)
            grid.attach(button2, 31, countries.index(country), 20, 1)

            self.box.add(grid)

    def combo_connecting(self, combo):
        iter = combo.get_active_iter()  # iter is a TreeIter object
        if iter is not None:
            model = combo.get_model()
            place = model[iter][0]
            if place != '-- Cities --':
                self.connecting(self, place.lower().replace(" ", "_"))

    def connecting(self, source, place):
        debug_print("=== connecting: " + place)
        connection(place)
        self.close()
