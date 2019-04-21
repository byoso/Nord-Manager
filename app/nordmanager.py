#!/usr/bin/env python3
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import Gtk, AppIndicator3
import os


class Indicator():
    def __init__(self):
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

    def create_menu(self):
        menu = Gtk.Menu()

        # menu items
        item_1 = Gtk.MenuItem('Custom Connexion')
        item_2 = gtk.MenuItem('Settings')
        item_us = gtk.MenuItem('USA')
        item_jp = gtk.MenuItem('Japan')
        item_ireland = gtk.MenuItem('Ireland')
        item_fr = gtk.MenuItem('France')
        item_iceland = gtk.MenuItem('Iceland')
        # Stop VPN
        item_stop = Gtk.MenuItem('** Close VPN **')
        #Quit
        item_quit = Gtk.MenuItem('Quit')

        # connect to callbacks
        item_1.connect('activate', self.connect_custom)
        item_us.connect('activate', self.connect_us)
        item_jp.connect('activate', self.connect_jp)
        item_ireland.connect('activate', self.connect_ireland)
        item_fr.connect('activate', self.connect_fr)
        item_iceland.connect('activate', self.connect_iceland)

        item_stop.connect('activate', self.connect_stop)

        item_quit.connect('activate', self.quit)


        # item_about.connect('activate', self.about)

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
        menu.append(item_2)
        # separator
        menu_sep_2 = Gtk.SeparatorMenuItem()
        menu.append(menu_sep_2)
        # quit
        menu.append(item_quit)

        menu.show_all()
        return menu

    # Callbacks    
    def quit(self, source):
        Gtk.main_quit()

    def connect_custom(self, source):
        with open(self.vpn_command, "r") as fichier:
            commande = fichier.read()
        os.system(commande)
        os.system("notify-send 'Trying to connect to custom'")

    def connect_us(self, source):
        os.system("nordvpn c us")
        os.system("notify-send 'Trying to connect to USA'")

    def connect_jp(self, source):
        os.system("nordvpn c jp")
        os.system("notify-send 'Trying to connect to Japan'")

    def connect_ireland(self, source):
        os.system("nordvpn c ireland")
        os.system("notify-send 'Trying to connect to Ireland'")

    def connect_fr(self, source):
        os.system("nordvpn c fr")
        os.system("notify-send 'Trying to connect to France'")

    def connect_iceland(self, source):
        os.system("nordvpn c iceland")
        os.system("notify-send 'Trying to connect to Iceland'")

    def connect_stop(self, source):
        os.system("nordvpn d")
        os.system("notify-send '!!!! VPN disconnected !!!!'")



Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
