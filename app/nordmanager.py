#!/usr/bin/env python3

import signal
import re
import gi
import os
import time
import json
from threading import Thread

gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import AyatanaAppIndicator3 as AppIndicator
from gi.repository import (
    Gtk,
    GdkPixbuf
    )

from toolbox import (
    license_BSD,
    load_data,
    record_data,
    BASE_DIR,
    shortcut_connection,
    debug_print,
)
from helpers import (
    IconMenuItem,
)
from browser import Browser
from config import __version__


data = load_data()


class IndicatorApp():
    def __init__(self):
        self.timing = int(data["timing"])
        debug_print("timing:" + str(self.timing))
        self.do_run = True
        self.ex_status = False
        app = 'Nord VPN Manager'
        iconpath = os.path.join(BASE_DIR, "icon_nordvpn_red.png")
        self.indicator = AppIndicator.Indicator.new(
            app, iconpath,
            AppIndicator.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        Thread(target=self.timer).start()

    def create_menu(self):
        menu = Gtk.Menu()

        # menu items*
        self.item_browse = Gtk.MenuItem(label="Browse...")
        self.item_1 = Gtk.MenuItem(label=data["it1n"])
        self.item_2 = Gtk.MenuItem(label=data["it2n"])
        self.item_3 = Gtk.MenuItem(label=data["it3n"])
        self.item_4 = Gtk.MenuItem(label=data["it4n"])
        self.item_5 = Gtk.MenuItem(label=data["it5n"])
        self.item_6 = Gtk.MenuItem(label=data["it6n"])

        # Stop VPN
        item_stop = IconMenuItem("network-offline", 'Close VPN connection')

        # settings
        item_settings = IconMenuItem("preferences-other", 'Settings')

        # Quit
        item_quit = IconMenuItem("process-stop", 'Quit')

        # connect to callbacks
        self.item_browse.connect('activate', self.connect_browse)
        self.item_1.connect('activate', self.connect_item1)
        self.item_2.connect('activate', self.connect_item2)
        self.item_3.connect('activate', self.connect_item3)
        self.item_4.connect('activate', self.connect_item4)
        self.item_5.connect('activate', self.connect_item5)
        self.item_6.connect('activate', self.connect_item6)

        item_stop.connect('activate', self.connect_stop)
        item_settings.connect('activate', self.settings)
        item_quit.connect('activate', self.quit)

        # menu placing
        menu_sep_browser = Gtk.SeparatorMenuItem()
        menu.append(self.item_browse)
        menu.append(menu_sep_browser)
        menu.append(self.item_1)
        menu.append(self.item_2)
        menu.append(self.item_3)
        menu.append(self.item_4)
        menu.append(self.item_5)
        menu.append(self.item_6)

        # Stop vpn
        menu.append(item_stop)
        # separator
        menu_sep_1 = Gtk.SeparatorMenuItem()
        menu_sep_2 = Gtk.SeparatorMenuItem()
        menu.append(menu_sep_1)
        menu.append(item_settings)
        menu.append(menu_sep_2)

        menu.append(item_quit)

        menu.show_all()
        return menu

    # Callbacks

    def quit(self, source):
        self.do_run = False
        Gtk.main_quit()

    def connect_browse(self, source):
        window = Browser()
        window.show_all()

    def connect_item1(self, source):
        commande = data["it1c"]
        shortcut_connection(commande)

    def connect_item2(self, source):
        commande = data["it2c"]
        shortcut_connection(commande)

    def connect_item3(self, source):
        commande = data["it3c"]
        shortcut_connection(commande)

    def connect_item4(self, source):
        commande = data["it4c"]
        shortcut_connection(commande)

    def connect_item5(self, source):
        commande = data["it5c"]
        shortcut_connection(commande)

    def connect_item6(self, source):
        commande = data["it6c"]
        shortcut_connection(commande)

    def connect_stop(self, source):
        os.system("nordvpn d")

    def settings(self, source):
        window = Settings()
        window.show_all()

    def timer(self):
        time.sleep(self.timing)
        debug_print("timer !!")
        self.status()

    def status(self):
        reg = os.popen(data["info_command"]).readlines()
        debug_print(reg)

        self.item_1.set_label(data["it1n"])
        self.item_2.set_label(data["it2n"])
        self.item_3.set_label(data["it3n"])
        self.item_4.set_label(data["it4n"])
        self.item_5.set_label(data["it5n"])
        self.item_6.set_label(data["it6n"])
        self.timing = int(data["timing"])

        status = False
        debug_print("green_word : " + data["green_word"])
        for i in reg:
            if data["green_word"] in i.lower():
                debug_print("i : " + i.lower())
                status = True
                break

        if status:
            debug_print("connected")
            self.indicator.set_icon_full(
                icon_name=os.path.join(BASE_DIR, "icon_nordvpn_green.png"),
                icon_desc="Nord-Manager")
            if self.ex_status != status:
                self.info_conn = ""
                for i in reg:
                    self.info_conn += "{}".format(i)

        else:
            debug_print("disconnected")
            self.indicator.set_icon_full(
                icon_name=os.path.join(BASE_DIR, "icon_nordvpn_red.png"),
                icon_desc="Nord-Manager")
            os.system(data["emergency"])

        self.ex_status = status

        if self.do_run:
            Thread(target=self.timer).start()


class Settings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Nord Manager Settings ({})".format(__version__))
        # init some values
        self.info_conn = ""
        reg = os.popen(data["info_command"]).readlines()
        for line in reg:
            m = re.match('([a-zA-Z])', line)
            if m is not None and "-" not in line:
                self.info_conn += "{}".format(line)
        # set the window
        self.set_properties(border_width=10)
        self.set_default_size(800, 600)
        self.set_size_request(400, 400)

        # scrolling window
        scroll = Gtk.ScrolledWindow()
        self.add(scroll)

        viewport = Gtk.Viewport()
        scroll.add(viewport)

        # boxes
        box = Gtk.HBox()
        box.set_homogeneous(True)
        box.set_spacing(20)
        viewport.add(box)
        lbox = Gtk.VBox()
        box.add(lbox)
        rbox = Gtk.VBox()
        box.add(rbox)

        # Frame info
        frame_info = Gtk.Frame()
        frame_info.set_label("Curent VPN connection informations")

        rbox.pack_start(frame_info, False, False, 10)

        info = Gtk.Label(label=self.info_conn)
        info.set_selectable(True)
        frame_info.add(info)

        # items frame
        it_frame = Gtk.Frame()
        it_frame.set_label("Buttons settings")
        itb = Gtk.VBox()
        it_frame.add(itb)

        # item 1
        it1l = Gtk.Label(label='Button 1:')
        self.it1ne = Gtk.Entry()
        self.it1ne.set_placeholder_text("button name")
        self.it1ne.set_text(data["it1n"])
        self.it1ce = Gtk.Entry()
        self.it1ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it1ce.set_text(data["it1c"])
        itb.pack_start(it1l, False, False, 0)
        itb.pack_start(self.it1ne, False, False, 0)
        itb.pack_start(self.it1ce, False, False, 5)

        # item 2
        it2l = Gtk.Label(label='Button 2:')
        self.it2ne = Gtk.Entry()
        self.it2ne.set_placeholder_text("button name")
        self.it2ne.set_text(data["it2n"])
        self.it2ce = Gtk.Entry()
        self.it2ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it2ce.set_text(data["it2c"])
        itb.pack_start(it2l, False, False, 0)
        itb.pack_start(self.it2ne, False, False, 0)
        itb.pack_start(self.it2ce, False, False, 5)

        # item 3
        it3l = Gtk.Label(label='Button 3:')
        self.it3ne = Gtk.Entry()
        self.it3ne.set_placeholder_text("button name")
        self.it3ne.set_text(data["it3n"])
        self.it3ce = Gtk.Entry()
        self.it3ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it3ce.set_text(data["it3c"])
        itb.pack_start(it3l, False, False, 0)
        itb.pack_start(self.it3ne, False, False, 0)
        itb.pack_start(self.it3ce, False, False, 5)

        # item 4
        it4l = Gtk.Label(label='Button 4:')
        self.it4ne = Gtk.Entry()
        self.it4ne.set_placeholder_text("button name")
        self.it4ne.set_text(data["it4n"])
        self.it4ce = Gtk.Entry()
        self.it4ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it4ce.set_text(data["it4c"])
        itb.pack_start(it4l, False, False, 0)
        itb.pack_start(self.it4ne, False, False, 0)
        itb.pack_start(self.it4ce, False, False, 5)

        # item 5
        it5l = Gtk.Label(label='Button 5:')
        self.it5ne = Gtk.Entry()
        self.it5ne.set_placeholder_text("button name")
        self.it5ne.set_text(data["it5n"])
        self.it5ce = Gtk.Entry()
        self.it5ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it5ce.set_text(data["it5c"])
        itb.pack_start(it5l, False, False, 0)
        itb.pack_start(self.it5ne, False, False, 0)
        itb.pack_start(self.it5ce, False, False, 5)

        # item 6
        it6l = Gtk.Label(label='Button 6:')
        self.it6ne = Gtk.Entry()
        self.it6ne.set_placeholder_text("button name")
        self.it6ne.set_text(data["it6n"])
        self.it6ce = Gtk.Entry()
        self.it6ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it6ce.set_text(data["it6c"])
        itb.pack_start(it6l, False, False, 0)
        itb.pack_start(self.it6ne, False, False, 0)
        itb.pack_start(self.it6ce, False, False, 5)

        lbox.pack_start(it_frame, False, False, 10)

        # Emergency setting
        self.emergency_label = Gtk.Label(
            label="Emergency kill (command if the VPN is disconnected)")
        self.emergency_entry = Gtk.Entry()
        help = """
        Please enter a bash command
        (eg: killall transmission-gtk)
        """
        self.emergency_entry.set_text(data["emergency"])
        self.emergency_entry.set_tooltip_text(help)
        self.emergency_label.set_tooltip_text(help)
        lbox.pack_start(self.emergency_label, False, False, 10)
        lbox.pack_start(self.emergency_entry, False, False, 10)

        # Save settings button
        save_button = Gtk.Button.new_from_icon_name(Gtk.STOCK_SAVE, 1)
        save_button.set_label("Save settings")
        save_button.set_always_show_image(True)
        save_button.connect('clicked', self.save_data)
        lbox.pack_end(save_button, False, False, 10)

        # advanced settings
        addvanced_frame = Gtk.Frame()
        addvanced_frame.set_label("Advanced settings")
        addvanced_frame_b = Gtk.VBox()
        addvanced_frame.add(addvanced_frame_b)
        rbox.pack_start(addvanced_frame, False, False, 10)

        # TIMING
        timing_l = Gtk.Label(label='timing (cycle duration):')
        self.timing = Gtk.SpinButton()
        self.timing.set_numeric(True)
        self.timing.set_range(1, 30)
        self.timing.set_increments(1, -1)
        self.timing.set_value(data["timing"])
        addvanced_frame_b.pack_start(timing_l, False, False, 0)
        addvanced_frame_b.pack_start(self.timing, False, False, 5)

        # green_word
        green_word_l = Gtk.Label(label='Green word (triggers the green status):')
        self.green_word = Gtk.Entry()
        self.green_word.set_text(data["green_word"])
        addvanced_frame_b.pack_start(green_word_l, False, False, 0)
        addvanced_frame_b.pack_start(self.green_word, False, False, 5)

        # info_command
        info_command_l = Gtk.Label(
            label='Info command (returns the VPN conection infos):')
        self.info_command = Gtk.Entry()
        self.info_command.set_text(data["info_command"])
        addvanced_frame_b.pack_start(info_command_l, False, False, 0)
        addvanced_frame_b.pack_start(self.info_command, False, False, 5)

        # Back to default
        default_button = Gtk.Button(label="Load default values")
        default_button.set_always_show_image(True)
        default_button.connect('clicked', self.default_data)
        rbox.pack_end(default_button, False, False, 10)

        # about
        about_button = Gtk.Button.new_from_icon_name(Gtk.STOCK_ABOUT, 1)
        about_button.set_label("About")
        about_button.set_always_show_image(True)
        about_button.connect('clicked', self.about)
        rbox.pack_end(about_button, False, False, 10)

    def about(self, widget):
        debug_print("about clicked !")
        dialog = PopUpAbout(self)
        dialog.run()
        dialog.destroy()

    def save_data(self, widget):
        try:
            nbr = int(self.timing.get_text())
            assert nbr > 0
            message = "ok"
        except AssertionError:
            message = "ERROR: timing must be greater than 0."
        except:  # TODO:missing except clause
            message = "ERROR: timing must be a number"

        finally:
            if message == "ok":
                data["it1n"] = self.it1ne.get_text()
                data["it1c"] = self.it1ce.get_text()
                data["it2n"] = self.it2ne.get_text()
                data["it2c"] = self.it2ce.get_text()
                data["it3n"] = self.it3ne.get_text()
                data["it3c"] = self.it3ce.get_text()
                data["it4n"] = self.it4ne.get_text()
                data["it4c"] = self.it4ce.get_text()
                data["it5n"] = self.it5ne.get_text()
                data["it5c"] = self.it5ce.get_text()
                data["it6n"] = self.it6ne.get_text()
                data["it6c"] = self.it6ce.get_text()
                data["emergency"] = self.emergency_entry.get_text()
                data["timing"] = self.timing.get_value()
                data["green_word"] = self.green_word.get_text()
                data["info_command"] = self.info_command.get_text()
                data["not_logged_in"] = "not logged in"
                record_data(data)
                os.system("notify-send 'Nord Manager: settings saved'")
            else:
                os.system("notify-send '{}'".format(message))

    def default_data(self, widget):

        default_data = os.path.join(BASE_DIR, "default_data.json")
        with open(default_data, 'r') as file:
            default_data = json.load(file)

        self.it1ne.set_text(default_data["it1n"])
        self.it1ce.set_text(default_data["it1c"])
        self.it2ne.set_text(default_data["it2n"])
        self.it2ce.set_text(default_data["it2c"])
        self.it3ne.set_text(default_data["it3n"])
        self.it3ce.set_text(default_data["it3c"])
        self.it4ne.set_text(default_data["it4n"])
        self.it4ce.set_text(default_data["it4c"])
        self.it5ne.set_text(default_data["it5n"])
        self.it5ce.set_text(default_data["it5c"])
        self.it6ne.set_text(default_data["it6n"])
        self.it6ce.set_text(default_data["it6c"])
        self.emergency_entry.set_text(default_data["emergency"])
        self.timing.set_value(default_data["timing"])
        self.green_word.set_text(default_data["green_word"])
        self.info_command.set_text(default_data["info_command"])


class PopUpAbout(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(
            self, "About Nord Manager", parent, Gtk.DialogFlags.MODAL)
        # self.set_size_request(300,400)
        self.set_comments("Non official Nord VPN Manager GUI")
        self.set_logo(
            GdkPixbuf.Pixbuf.new_from_file(os.path.join(BASE_DIR, "Peigne-plume-256-320.png")))
        self.set_copyright(
            "Copyright 2019 Fabre Vincent <peigne.plume@gmail.com>")
        self.set_version(__version__)
        self.set_authors(["Vincent Fabre, <peigne.plume@gmail.com>"])
        self.set_license_type(Gtk.License.BSD)
        self.set_program_name("Nord Manager")
        self.set_license(license_BSD)

        self.show_all()


IndicatorApp()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
