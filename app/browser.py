
import gi
import os

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from toolbox import reg, load_data, connection



class Browser(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Nord Manager browser")
        # headerbar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.set_title("Nord Manager browser")
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

        text = os.popen('nordvpn countries')
        countries = reg(text)

        # boxes
        self.box = Gtk.VBox()
        self.viewport.add(self.box)

        for country in countries:
            box = Gtk.HBox()
            # gbox = Gtk.Grid()
            button = Gtk.Button(country)
            print(country)#debug
            # os.system("notify-send 'country : {}'".format(country))#debug
            cities = reg(os.popen("nordvpn cities {}".format(country)))
            print(cities)#debug
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

            box.pack_start(button, False, True, 10)

            button.connect('clicked', self.connecting, country)
            box.pack_end(button2, False, False, 10)

            self.box.pack_start(box, True, True, 0)

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
