![nordvpn](https://lh3.googleusercontent.com/fYdbiwmBnCVn27ZUaGez84Q_F1F59cHpD3La-KpJmmhj9uAvtQaes72cbBTIt2n8gVjJAz0cEx5yAhM6H5Ou8D_T=w128-h128-e365-rj-sc0x00ffffff)

# Nord Manager

_Non official NordVPN GUI for linux_


Very light weight application, simple and fast GUI.
A security option the closes the transmission app if the vpn is
disconnected.

 :coffee: [**You can buy me a coffee if you're in the mood ;)**](https://www.buymeacoffee.com/byoso)

## INSTALLATION (on any linux distro)

Now Nord Manager uses ayatana appindicator for better compatibility. It is supposed to be included in most of the recent major distros,
but depending on the system you are you running, this dependencie may be missing. You can install it this way:

**Example for Ubuntu**:
```bash
$ sudo apt install gir1.2-ayatanaappindicator3-0.1
```

Then:

- be sure you have the official nordvpn installed first.

- So you can install nord manager:
```bash
$ ./installer
```
Then follow the instructions
- if the installer asks you to install pip, do not forget to reboot after installing pip, before running the installer again.

Uninstall:
```bash
$ geninstaller uninstall 'Nord Manager'
```

## Main functionalities :

- **Browse...** : opens a window showing all the available servers, you just
have to pick the one you want, fast and easy.

- **6 shortcuts buttons** : this buttons are already set with default values,
but are expected to be customized to your own needs,
you can set them in the settings window. Each button is defined by 2 fileds,
the first is the name you want for your button, the second is the bash
command line to execute when clicked. Any bash command you set here
will be executed when clicked, but the console will not be shown.



## Settings explained:

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
not connected, typicaly :
```
killall transmission-gtk
```
You can chain commands with ";" if you want to kill multiple applications e.g:
```
killall transmission-gtk; killall amule;
```
You can simply
deactivate it by commenting the line ("#" at the begining)


### Changelog:
- 2.1.3 : Timeout for some actions, so the app wont get stuck anymore if a call do not receive a response fom nord vpn's servers.
- 2.1.0 : use of nord vpn's api instead of "scrapping" the terminal to get the countries and cities (more reliable)
- 2.0.2 : Autodetect if not logged in, then redirect to the connection web page.
