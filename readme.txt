Nord Manager (GUI for nordvpn)

===================================================================

- What is it :

This is a complete Nord VPN unoffical GUI, it also offer a security
option to close the transmission app if the vpn is disconnected.

As it is a very light weight applicatin, i suggest you set it to be 
launched automaticly when the system starts.

===================================================================

- To install :
./install.sh
enter your admin code, and then it works.

- To uninstall :
./uninstall.sh
and that's all !

====================================================================

- Settings explained:

- In the directory ~/.local/share/NordManager you will find a file
named "data.json", it contains the settings of the app.

Change it to the command adapted to your own needs.
don't forget to RTFM : man nordvpn
;)

- info_command : the bash command to get the status of the vpn. For
nord VPN it is "nordvpn status"

- green word : by default it is " connected" (note the space before the 
word, otherwise there will be a confusion with the "disconnected" string.
The green word triggers the green status of the app if detected in 
the current VPN connection information.

- timing : the length of the cycle between status checks, by default
it is 4 (seconds).

- emmergency kill :
This is a bash command that prevent the use of some app if the VPN is
not connected, typicaly : "killall transmission-gtk". You can simply
deactivate it by commenting the line ("#" at the begining)

====================================================================
- Contact me (for any good reason):

If you want to contact me, i'm quite easy to join :
Vincent Fabre
<peigne-plume-at-gmail.com>





