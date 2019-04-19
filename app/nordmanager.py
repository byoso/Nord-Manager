#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import os


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
