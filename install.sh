#!/bin/bash

# =============== PIXMAPS
sudo cp app/icon_nordvpn.png /usr/share/pixmaps/
sudo cp app/icon_nordvpn_red.png /usr/share/pixmaps/
sudo cp app/icon_nordvpn_green.png /usr/share/pixmaps/



# =============== APPLICATIONS
sudo cp app/NordManager.desktop /usr/share/applications/


# =============== /usr/bin/
sudo cp app/nordmanager.sh /usr/bin/


# =============== /OPT/NORDMANAGER
sudo mkdir -p /opt/NordManager/
sudo cp app/nordmanager.py /opt/NordManager/


# =============== settings files
sudo mkdir -p ~/.local/share/NordManager/
sudo cp app/vpn_command.txt ~/.local/share/NordManager/


# =============== RIGHTS
sudo chmod -R 755 ~/.local/share/NordManager
sudo chown -R $USER ~/.local/share/NordManager

echo "Installation completed, please read the readme file to know more"


