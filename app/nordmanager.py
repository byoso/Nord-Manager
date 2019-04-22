#!/usr/bin/env python3
import signal
import gi
import os
import time
import json
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import Gtk, AppIndicator3
from threading import Thread


info_conn = ""

#========== Some globaly used functions ===========

local_rep = os.path.expanduser("~/.local/share/NordManager/")
data_file = os.path.join(local_rep, "data.json")


def record_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)


def load_data():
    with open(data_file, 'r') as file:
        data = json.load(file)
    return data

data = load_data()

# ================= Classes used ==================


class Indicator():
    def __init__(self):
        timing = 4
        info_conn = "truc"
        self.do_run = True
        self.ex_status = False
        # local_rep = os.path.expanduser("~/.local/share/NordManager/")
        # self.vpn_command = local_rep + "vpn_command.txt"
        app = 'Nord VPN Manager'
        iconpath = "/usr/share/pixmaps/icon_nordvpn_red.png"
        self.indicator = AppIndicator3.Indicator.new(
            app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("Nord VPN Manager", app)
        Thread(target=self.timer).start()

    def create_menu(self):
        menu = Gtk.Menu()

        # menu items
        self.item_1 = Gtk.MenuItem("-- "+data["custom_name"]+" --")
        item_settings = gtk.MenuItem('Settings')
        item_us = gtk.MenuItem('USA')
        item_jp = gtk.MenuItem('Japan')
        item_ireland = gtk.MenuItem('Ireland')
        item_fr = gtk.MenuItem('France')
        item_iceland = gtk.MenuItem('Iceland')
        # Stop VPN
        item_stop = Gtk.MenuItem('** Close VPN connection **')
        # Quit
        item_quit = Gtk.MenuItem('Quit')

        # connect to callbacks
        self.item_1.connect('activate', self.connect_custom)

        item_settings.connect('activate', self.settings)

        item_us.connect('activate', self.connect_us)
        item_jp.connect('activate', self.connect_jp)
        item_ireland.connect('activate', self.connect_ireland)
        item_fr.connect('activate', self.connect_fr)
        item_iceland.connect('activate', self.connect_iceland)

        item_stop.connect('activate', self.connect_stop)

        item_quit.connect('activate', self.quit)

        # menu placing
        menu.append(self.item_1)
        menu.append(item_us)
        menu.append(item_jp)
        menu.append(item_ireland)
        menu.append(item_fr)
        menu.append(item_iceland)
        # Stop vpn
        menu.append(item_stop)
        # separator
        menu_sep_1 = Gtk.SeparatorMenuItem()
        menu.append(menu_sep_1)
        menu.append(item_settings)
        # separator
        menu_sep_2 = Gtk.SeparatorMenuItem()
        menu.append(menu_sep_2)
        # quit
        menu.append(item_quit)

        menu.show_all()
        return menu

    # Callbacks

    def quit(self, source):
        self.do_run = False
        Gtk.main_quit()

    def connect_custom(self, source):
        commande = data["custom"]
        os.system(commande)
        # os.system("notify-send 'Trying to connect to custom'")

    def connect_us(self, source):
        os.system("nordvpn c us")
        # os.system("notify-send 'Trying to connect to USA'")

    def connect_jp(self, source):
        os.system("nordvpn c jp")
        # os.system("notify-send 'Trying to connect to Japan'")

    def connect_ireland(self, source):
        os.system("nordvpn c ireland")
        # os.system("notify-send 'Trying to connect to Ireland'")

    def connect_fr(self, source):
        os.system("nordvpn c fr")
        # os.system("notify-send 'Trying to connect to France'")

    def connect_iceland(self, source):
        os.system("nordvpn c iceland")
        # os.system("notify-send 'Trying to connect to Iceland'")

    def connect_stop(self, source):
        os.system("nordvpn d")
        os.system("notify-send '!!!! VPN disconnected !!!!'")

    def settings(self, source):
        window = Settings()
        window.show_all()

    def timer(self, timing=4):
        time.sleep(timing)
        print("timer !!")
        self.status()

    def status(self):
        reg = os.popen("nordvpn status").readlines()
        print(reg)

        self.item_1.set_label(data["custom_name"])

        status = True

        for i in reg:
            if "Disconnected" in i:
                status = False

        if status:
            print("connected")
            self.indicator.set_icon(
                "/usr/share/pixmaps/icon_nordvpn_green.png")
            # Notify connexion settnigs when new connection
            if self.ex_status != status:
                self.info_conn = ""
                for i in reg:
                    self.info_conn += "{}".format(i)
                os.system("notify-send '{}'".format(self.info_conn))

        else:
            print("disconnected")
            self.indicator.set_icon("/usr/share/pixmaps/icon_nordvpn_red.png")
            os.system(data["emergency"])

        self.ex_status = status

        if self.do_run:
            Thread(target=self.timer).start()


class Settings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Nord Manager Settings")
        # init some values
        self.info_conn = ""
        reg = os.popen("nordvpn status").readlines()
        for i in reg:
            self.info_conn += "{}\n".format(i)
        # set the window
        self.set_properties(border_width=10)
        self.set_size_request(700, 400)

        # layout
        box = gtk.HBox()
        box.set_homogeneous(True)
        box.set_spacing(10)
        self.add(box)
        lbox = gtk.VBox()
        box.add(lbox)
        rbox = gtk.VBox()
        box.add(rbox)
        frame_info = gtk.Frame()
        frame_info.set_label("Curent VPN connection informations")

        lbox.pack_start(frame_info, False, False, 10)

        info = gtk.Label(self.info_conn)
        info.set_selectable(True)
        frame_info.add(info)

        # Custom_name setting

        self.custom_name_label = gtk.Label("Choose a connection name:")
        self.custom_name = Gtk.Entry()
        help_name = """
        Please enter a bash command
        (eg: Hong Kong) and press ENTER
        """
        self.custom_name.set_text(data["custom_name"])
        self.custom_name.set_tooltip_text(help_name)
        self.custom_name_label.set_tooltip_text(help_name)

        # Custom entry setting
        self.custom_label = gtk.Label("Custom connection command:")
        self.custom_entry = Gtk.Entry()
        help = """
        Please enter a bash command
        (eg: nordvpn c hk) and press ENTER
        """
        self.custom_entry.set_text(data["custom"])
        self.custom_entry.set_tooltip_text(help)
        self.custom_label.set_tooltip_text(help)

        rbox.pack_start(self.custom_name_label, False, False, 10)
        rbox.pack_start(self.custom_name, False, False, 10)
        rbox.pack_start(self.custom_label, False, False, 10)
        rbox.pack_start(self.custom_entry, False, False, 10)

        # Emergency setting
        self.emergency_label = gtk.Label(
            "Emergency command if the VPN is disconnected")
        self.emergency_entry = Gtk.Entry()
        help = """
        Please enter a bash command
        (eg: killall -9 transmission-gtk) and press ENTER
        """
        self.emergency_entry.set_text(data["emergency"])
        self.emergency_entry.set_tooltip_text(help)
        self.emergency_label.set_tooltip_text(help)
        rbox.pack_start(self.emergency_label, False, False, 10)
        rbox.pack_start(self.emergency_entry, False, False, 10)

        # Save settings button
        save_button = Gtk.Button.new_from_stock(Gtk.STOCK_SAVE)
        save_button.set_always_show_image(True)
        save_button.connect('clicked', self.save_data)
        rbox.pack_start(save_button, False, False, 10)

    def save_data(self, widget):
        data["custom"] = self.custom_entry.get_text()
        data["custom_name"] = self.custom_name.get_text()
        data["emergency"] = self.emergency_entry.get_text()
        record_data(data)
        os.system("notify-send 'data recorded'")


indic = Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
