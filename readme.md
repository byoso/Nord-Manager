# Nord Manager (Linux GUI for nordvpn)



- What is it :

This is a complete Nord VPN unoffical GUI for Linux, it also offers
a security option to close the transmission app if the vpn is
disconnected.

As it is a very light weight application, I suggest you set it to be
launched automaticly when the system starts, or not, works fine with
a shortcut too.


## INSTALLATION

(be sure you have the official nordvpn installed first).

### DEBIAN, UBUNTU, MINT... :

- To install :
```bash
./install.sh
```
enter your admin code, and then it works.

- To uninstall :
```bash
./uninstall.sh
```
and that's all !


### NON DEBIAN BASED OS:
You will have to edit the install.sh to change the "apt" command
to your own package manager command.
GTK in also a required dependency.
If you still got an issue, please leave a post on github here:
https://github.com/byoso/Nord-Manager/issues


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
~/.local/share/NordManager
```
you will find a file
named "data.json", it contains the settings of the app.

Change it to the command adapted to your own needs.
don't forget to RTFM : man nordvpn
;)

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
