#!/usr/bin/env python3
import signal
import gi
import os
import time
import json
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import Gtk, AppIndicator3, GdkPixbuf
from threading import Thread
from toolbox import *


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
        self.timing = int(data["timing"])
        print("timing:" + str(self.timing))  # debug
        self.do_run = True
        self.ex_status = False
        app = 'Nord VPN Manager'
        iconpath = "/usr/share/pixmaps/icon_nordvpn_red.png"
        self.indicator = AppIndicator3.Indicator.new(
            app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        # self.indicator.set_label("Nord VPN Manager", app)
        Thread(target=self.timer).start()

    def create_menu(self):
        menu = Gtk.Menu()

        # menu items
        self.item_1 = Gtk.MenuItem(data["it1n"])
        self.item_2 = Gtk.MenuItem(data["it2n"])
        self.item_3 = Gtk.MenuItem(data["it3n"])
        self.item_4 = Gtk.MenuItem(data["it4n"])
        self.item_5 = Gtk.MenuItem(data["it5n"])
        self.item_6 = Gtk.MenuItem(data["it6n"])

        # Stop VPN
        item_stop = Gtk.ImageMenuItem('Close VPN connection')
        item_stop.set_image(Gtk.Image.new_from_icon_name("network-offline", Gtk.IconSize(5)))

        # settings
        item_settings = gtk.ImageMenuItem('Settings')
        item_settings.set_image(Gtk.Image.new_from_icon_name("preferences-other", Gtk.IconSize(5)))

        # Quit
        item_quit = Gtk.ImageMenuItem('Quit')
        item_quit.set_image(Gtk.Image.new_from_icon_name("process-stop", Gtk.IconSize(5)))


        # connect to callbacks
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
        # # separator
        # menu_sep_3 = Gtk.SeparatorMenuItem()
        # menu.append(menu_sep_3)
        # quit
        menu.append(item_quit)

        menu.show_all()
        return menu

    # Callbacks

    def quit(self, source):
        self.do_run = False
        Gtk.main_quit()

    def connect_item1(self, source):
        commande = data["it1c"]
        os.system(commande)

    def connect_item2(self, source):
        commande = data["it2c"]
        os.system(commande)

    def connect_item3(self, source):
        commande = data["it3c"]
        os.system(commande)

    def connect_item4(self, source):
        commande = data["it4c"]
        os.system(commande)

    def connect_item5(self, source):
        commande = data["it5c"]
        os.system(commande)

    def connect_item6(self, source):
        commande = data["it6c"]
        os.system(commande)

    def connect_stop(self, source):
        os.system("nordvpn d")
        os.system("notify-send '!!!! VPN disconnected !!!!'")

    def settings(self, source):
        window = Settings()
        window.show_all()

    def about(self, widget):#finally not used
        print("about clicked !")
        dialog = PopUpAbout(self)
        response = dialog.run()
        dialog.destroy()

    def timer(self):
        time.sleep(self.timing)
        print("timer !!")
        self.status()

    def status(self):
        reg = os.popen(data["info_command"]).readlines()
        print(reg)

        self.item_1.set_label(data["it1n"])
        self.item_2.set_label(data["it2n"])
        self.item_3.set_label(data["it3n"])
        self.item_4.set_label(data["it4n"])
        self.item_5.set_label(data["it5n"])
        self.item_6.set_label(data["it6n"])
        self.timing = int(data["timing"])

        status = False
        print("green_word : " + data["green_word"])  # debug
        for i in reg:
            if data["green_word"] in i.lower():
                print("i : " + i.lower())  # debug
                status = True
                break

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
        reg = os.popen(data["info_command"]).readlines()
        for i in reg:
            self.info_conn += "{}\n".format(i)
        # set the window
        self.set_properties(border_width=10)
        self.set_size_request(700, 600)

        # layout
        box = gtk.HBox()
        box.set_homogeneous(True)
        box.set_spacing(10)
        self.add(box)
        lbox = gtk.VBox()
        box.add(lbox)
        rbox = gtk.VBox()
        box.add(rbox)

        # Frame info
        frame_info = gtk.Frame()
        frame_info.set_label("Curent VPN connection informations")

        rbox.pack_start(frame_info, False, False, 10)

        info = gtk.Label(self.info_conn)
        info.set_selectable(True)
        frame_info.add(info)

        # items frame
        it_frame = gtk.Frame()
        it_frame.set_label("Buttons settings")
        itb = gtk.VBox()
        it_frame.add(itb)

        # item 1
        it1l = gtk.Label('Button 1:')
        self.it1ne = gtk.Entry()
        self.it1ne.set_placeholder_text("button name")
        self.it1ne.set_text(data["it1n"])
        self.it1ce = gtk.Entry()
        self.it1ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it1ce.set_text(data["it1c"])
        itb.pack_start(it1l, False, False, 0)
        itb.pack_start(self.it1ne, False, False, 0)
        itb.pack_start(self.it1ce, False, False, 5)

        # item 2
        it2l = gtk.Label('Button 2:')
        self.it2ne = gtk.Entry()
        self.it2ne.set_placeholder_text("button name")
        self.it2ne.set_text(data["it2n"])
        self.it2ce = gtk.Entry()
        self.it2ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it2ce.set_text(data["it2c"])
        itb.pack_start(it2l, False, False, 0)
        itb.pack_start(self.it2ne, False, False, 0)
        itb.pack_start(self.it2ce, False, False, 5)

        # item 3
        it3l = gtk.Label('Button 3:')
        self.it3ne = gtk.Entry()
        self.it3ne.set_placeholder_text("button name")
        self.it3ne.set_text(data["it3n"])
        self.it3ce = gtk.Entry()
        self.it3ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it3ce.set_text(data["it3c"])
        itb.pack_start(it3l, False, False, 0)
        itb.pack_start(self.it3ne, False, False, 0)
        itb.pack_start(self.it3ce, False, False, 5)

        # item 4
        it4l = gtk.Label('Button 4:')
        self.it4ne = gtk.Entry()
        self.it4ne.set_placeholder_text("button name")
        self.it4ne.set_text(data["it4n"])
        self.it4ce = gtk.Entry()
        self.it4ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it4ce.set_text(data["it4c"])
        itb.pack_start(it4l, False, False, 0)
        itb.pack_start(self.it4ne, False, False, 0)
        itb.pack_start(self.it4ce, False, False, 5)

        # item 5
        it5l = gtk.Label('Button 5:')
        self.it5ne = gtk.Entry()
        self.it5ne.set_placeholder_text("button name")
        self.it5ne.set_text(data["it5n"])
        self.it5ce = gtk.Entry()
        self.it5ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it5ce.set_text(data["it5c"])
        itb.pack_start(it5l, False, False, 0)
        itb.pack_start(self.it5ne, False, False, 0)
        itb.pack_start(self.it5ce, False, False, 5)

        # item 6
        it6l = gtk.Label('Button 6:')
        self.it6ne = gtk.Entry()
        self.it6ne.set_placeholder_text("button name")
        self.it6ne.set_text(data["it6n"])
        self.it6ce = gtk.Entry()
        self.it6ce.set_placeholder_text("bash command (eg : nordvpn c us)")
        self.it6ce.set_text(data["it6c"])
        itb.pack_start(it6l, False, False, 0)
        itb.pack_start(self.it6ne, False, False, 0)
        itb.pack_start(self.it6ce, False, False, 5)

        lbox.pack_start(it_frame, False, False, 10)

        # Emergency setting
        self.emergency_label = gtk.Label(
            "Emergency kill (command if the VPN is disconnected)")
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
        save_button = Gtk.Button.new_from_stock(Gtk.STOCK_SAVE)
        save_button.set_always_show_image(True)
        save_button.connect('clicked', self.save_data)
        lbox.pack_end(save_button, False, False, 10)

        # advanced settings
        addvanced_frame = gtk.Frame()
        addvanced_frame.set_label("Advanced settings")
        addvanced_frame_b = gtk.VBox()
        addvanced_frame.add(addvanced_frame_b)
        rbox.pack_start(addvanced_frame, False, False, 10)

        # TIMING
        timing_l = gtk.Label('timing (cycle duration):')
        self.timing = gtk.SpinButton()
        self.timing.set_numeric(True)
        self.timing.set_range(1, 30)
        self.timing.set_increments(1,-1)
        self.timing.set_value(data["timing"])
        addvanced_frame_b.pack_start(timing_l, False, False, 0)
        addvanced_frame_b.pack_start(self.timing, False, False, 5)

        # green_word
        green_word_l = gtk.Label('Green word (triggers the green status):')
        self.green_word = gtk.Entry()
        self.green_word.set_text(data["green_word"])
        addvanced_frame_b.pack_start(green_word_l, False, False, 0)
        addvanced_frame_b.pack_start(self.green_word, False, False, 5)

        # info_command
        info_command_l = gtk.Label(
            'Info command (returns the VPN conection infos):')
        self.info_command = gtk.Entry()
        self.info_command.set_text(data["info_command"])
        addvanced_frame_b.pack_start(info_command_l, False, False, 0)
        addvanced_frame_b.pack_start(self.info_command, False, False, 5)

        # Back to default
        default_button = Gtk.Button("Load default values")
        default_button.set_always_show_image(True)
        default_button.connect('clicked', self.default_data)
        rbox.pack_end(default_button, False, False, 10)

        #about
        about_button = Gtk.Button.new_from_stock(Gtk.STOCK_ABOUT)
        about_button.set_always_show_image(True)
        about_button.connect('clicked', self.about)
        rbox.pack_end(about_button, False, False, 10)


    def about(self, widget):
        print("about clicked !")
        dialog = PopUpAbout(self)
        response = dialog.run()
        dialog.destroy()


    def save_data(self, widget):
        try:
            nbr = int(self.timing.get_text())
            assert nbr > 0
            message = "ok"
        except AssertionError:
            message = "ERROR: timing must be greater than 0."
        except:
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
                record_data(data)
                os.system("notify-send 'Nord Manager: settings saved'")
            else:
                os.system("notify-send '{}'".format(message))

    def default_data(self, widget):

        default_data = os.path.join(local_rep, "default_data.json")
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
        Gtk.Dialog.__init__(self, "About Nord Manager", parent, Gtk.DialogFlags.MODAL)
        #self.set_size_request(300,400)
        self.set_comments("Non official Nord VPN Manager GUI")
        self.set_logo(GdkPixbuf.Pixbuf.new_from_file("/opt/NordManager/Peigne-plume-256-320.png"))
        self.set_copyright("Copyright 2019 Fabre Vincent <peigne.plume@gmail.com>")
        self.set_version("1.0")
        self.set_authors(["Vincent Fabre, <peigne.plume@gmail.com>"])
        self.set_license_type(Gtk.License.BSD)
        self.set_program_name("Nord Manager")
        self.set_license(license_BSD)

        self.show_all()


indic = Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
