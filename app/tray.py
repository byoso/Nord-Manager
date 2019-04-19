#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import os

APPINDICATOR_ID = 'myappindicator'


def main():
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID, Gtk.STOCK_YES, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    indicator.set_icon('modem')

    gtk.main()


def build_menu():
    menu = gtk.Menu()
    item_nord_command = gtk.MenuItem('Edit nordvpn command')
    item_nord_command.connect('activate', set_command)
    menu.append(item_nord_command)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def set_command(source):
    os.system("notify-send 'eg: nordvpn c us'")
    window.show_all()


def quit(source):
    with open("~/.local/share/NordManager/tray.txt",'w') as fichier:
        fichier.write("off")
    gtk.main_quit()


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.saisie = gtk.Entry()
        self.add(self.saisie)
        self.saisie.connect('activate', self.saisie_commande)

    def saisie_commande(self, widget):
        self.new_commande = self.saisie.get_text()
        self.hide()
        dossier = os.path.expanduser("~/.local/share/NordManager/")
        print(dossier)
        commande = dossier + "vpn_command.txt"
        with open(commande, 'w') as mon_fichier:
            mon_fichier.write(self.new_commande)
        return os.system("notify-send {}".format(self.new_commande))


window = MainWindow()
# window.connect("delete-event", Gtk.main_quit)
if __name__ == "__main__":
    main()
