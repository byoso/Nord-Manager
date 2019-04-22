#!/usr/bin/env python3
import signal
import gi
import os
import time
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import Gtk, AppIndicator3
from threading import Thread


info_conn = ""


class Indicator():
    def __init__(self):
        timing = 4
        info_conn = "truc"
        self.do_run = True
        self.ex_status = False
        local_rep = os.path.expanduser("~/.local/share/NordManager/")
        self.vpn_command = local_rep + "vpn_command.txt"
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
        item_1 = Gtk.MenuItem('Custom Connexion')
        item_settings = gtk.MenuItem('Settings')
        item_us = gtk.MenuItem('USA')
        item_jp = gtk.MenuItem('Japan')
        item_ireland = gtk.MenuItem('Ireland')
        item_fr = gtk.MenuItem('France')
        item_iceland = gtk.MenuItem('Iceland')
        # Stop VPN
        item_stop = Gtk.MenuItem('** Close VPN **')
        # Quit
        item_quit = Gtk.MenuItem('Quit')

        # connect to callbacks
        item_1.connect('activate', self.connect_custom)

        item_settings.connect('activate', self.settings)

        item_us.connect('activate', self.connect_us)
        item_jp.connect('activate', self.connect_jp)
        item_ireland.connect('activate', self.connect_ireland)
        item_fr.connect('activate', self.connect_fr)
        item_iceland.connect('activate', self.connect_iceland)

        item_stop.connect('activate', self.connect_stop)

        item_quit.connect('activate', self.quit)

        # menu placing
        menu.append(item_1)
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
        with open(self.vpn_command, "r") as fichier:
            commande = fichier.read()
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

        status = True

        for i in reg:
            if "Disconnected" in i:
                status = False

        if status:
            print("connecté")
            self.indicator.set_icon(
                "/usr/share/pixmaps/icon_nordvpn_green.png")
            # Notify connexion settnigs when new connection
            if self.ex_status != status:
                self.info_conn = ""
                for i in reg:
                    self.info_conn += "{}\n".format(i)
                os.system("notify-send '{}'".format(self.info_conn))

        else:
            print("déconnecté")
            self.indicator.set_icon("/usr/share/pixmaps/icon_nordvpn_red.png")

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
        self.set_size_request(250, 100)

        # layout
        box = gtk.VBox()
        self.add(box)
        info = gtk.Label(self.info_conn)
        info.set_selectable(True)
        box.pack_start(info, False, True, 10)

        self.custom_label = gtk.Label("Register a custom connexion")
        self.custom_entry = Gtk.Entry()
        help = """
        Please enter a bash command
        (eg: nordvpn c us) and press ENTER
        """
        self.custom_entry.set_text("nordvpn c us")
        self.custom_entry.set_tooltip_text(help)
        self.custom_label.set_tooltip_text(help)
        box.pack_start(self.custom_label, True, True, 0)
        box.pack_start(self.custom_entry, True, True, 0)

        self.custom_entry.connect('activate', self.custom_save)

    def custom_save(self, widget):
        print("======== TO DO SAVE ========")


indic = Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
