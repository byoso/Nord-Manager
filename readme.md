

![nordvpn](https://lh3.googleusercontent.com/fYdbiwmBnCVn27ZUaGez84Q_F1F59cHpD3La-KpJmmhj9uAvtQaes72cbBTIt2n8gVjJAz0cEx5yAhM6H5Ou8D_T=w128-h128-e365-rj-sc0x00ffffff)

# Nord Manager

_Non official NordVPN GUI for linux_


Very light weight application, simple and fast GUI.
A security option the closes the transmission app if the vpn is
disconnected.

### Version 2.0.0 (with the 'geninstaller' installer)
The only difference with the 1.5.0 is the installer. This new one will install by himself a few dependencies, but is cleaner, and should work fine with any linux distro, not only Ubuntu.
Feel free to e-mail me some feedback please (peigne.plume-at-gmail.com).
([informations about geninstaller here](https://github.com/byoso/geninstaller))

### Version 1.5.0 (with no 'geninstaller' installer)
Fix the bug caused by Nordvpn's add "New Feature ..."

[version 1.5.0 is available here](https://github.com/byoso/Nord-Manager/tree/master_1.5.0)

## INSTALLATION (Now on any linux distro)

(be sure you have the official nordvpn installed first).

Install:
```
./installer
```
(then follow the instructions)

Uninstall:
```
geninstaller uninstall 'Nord Manager'
```

## Main functionalities :

-Browse... : opens a window showing all the available servers, you just
have to pick the one you want, fast and easy.

- 6 shortcuts buttons : this buttons are already set with default values,
but are expected to be customized to your own needs,
you can set them in the settings window. Each button is defined by 2 fileds,
the first is the name you want for your button, the second is the bash
command line to execute when clicked. Any bash command you set here
will be executed when clicked, but the console will not be shown.



## Settings explained:

- In the **directory**
```
~/.local/share/applications-files/Nord_Manager
```
you will find the installed files.

- **info_command** : the bash command to get the status of the vpn. For
nord VPN it is "nordvpn status"

- **green word** : by default it is " connected" (note the space before the
word, otherwise there will be a confusion with the "disconnected" string).
The green word triggers the green status of the app if detected in
the current VPN connection information.

- **timing** : the length of the cycle between status checks, by default
it is 3 (seconds).

- **emmergency kill** :
This is a bash command that prevent the use of some app if the VPN is
not connected, typicaly : "killall transmission-gtk". You can simply
deactivate it by commenting the line ("#" at the begining)


### Contact
- Contact me (for any good reason):

If you want to contact me, i'm quite easy to join :
Vincent Fabre
peigne.plume-at-gmail.com
