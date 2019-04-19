#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import os
import subprocess


dossier = os.path.expanduser("~/.local/share/NordManager/")
print(dossier)
fichier = dossier + "data.txt"
commande = dossier + "vpn_command.txt"
print(fichier)

with open(commande, 'r') as mon_fichier:
    commande = mon_fichier.read()


with open(fichier, 'r') as mon_fichier:
    state = mon_fichier.read()

print(state)

#======= Gestion du system tray
# il ne doit etre present qu'une seule fois
tray = dossier + "tray.txt"
with open(tray, 'r') as mon_fichier:
    tray_state = mon_fichier.read()

if tray_state == "on":
    pass
if tray_state == "off":
    subprocess.call("/opt/NordManager/tray.py")
    with open(tray, 'w') as mon_fichier:
        mon_fichier.write("off")


#======== Gestion du ON / OFF du VPN

if state == 'false':
    os.system("notify-send 'VPN ON'")
    os.system(commande)
    with open(fichier, 'w') as mon_fichier:
        mon_fichier.write('true')

else:
    os.system("notify-send 'VPN OFF'")
    os.system("nordvpn d")
    with open(fichier, 'w') as mon_fichier:
        mon_fichier.write('false')


# a = input("PRESS ENTER TO CLOSE")
