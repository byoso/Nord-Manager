#!/bin/bash

sudo cp app/icon_nordvpn.png /usr/share/pixmaps/

sudo cp app/NordManager.desktop /usr/share/applications/

sudo cp app/nordmanager.sh /usr/bin/

sudo mkdir -p /opt/NordManager/
sudo cp app/nordmanager.py /opt/NordManager/
sudo cp app/tray.py /opt/NordManager/


sudo mkdir -p ~/.local/share/NordManager/
sudo cp app/data.txt ~/.local/share/NordManager/
sudo cp app/vpn_command.txt ~/.local/share/NordManager/
sudo cp app/tray.txt ~/.local/share/NordManager/

sudo chmod -R 755 ~/.local/share/NordManager
sudo chown -R $USER ~/.local/share/NordManager

echo "Installation completed, please read the readme file to know more"


