#!/bin/bash

# =============== ICONES
sudo rm /usr/share/pixmaps/icon_nordvpn.png
sudo rm /usr/share/pixmaps/icon_nordvpn_red.png
sudo rm /usr/share/pixmaps/icon_nordvpn_green.png


# =============== Applications
sudo rm /usr/share/applications/NordManager.desktop

# =============== /USR/BIN
sudo rm /usr/bin/nordmanager.sh

# =============== /OPT
sudo rm -r /opt/NordManager/


# =============== local files
sudo rm -r ~/.local/share/NordManager/


echo "Uninstallation done, your system is clean from NordManager"


