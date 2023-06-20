# pyNotify
A gnome (wayland) notifier for Gotify server
Gotify server is open source software for notifications that can be deployed on-prem (self-hosted). 
It provides web based service, API,  and also mobile application, but I was missing a working gnome tray notification app for receiving those notifications directly in my gnome desktop (wayland), so I build this.

NOTE: "Exit" from system tray icon menu is not working (still under investigation)

## Installation
Download the release package and copy itś contents to /opt/pyNotify. 
This release package has a binary already compiled and ready to execute on Linux.
The bash script (install.sh) inside the realease package will copy all the necessary files to /opt/pyNotify in one go.....
....just edit the file pyNotify.conf in that destination folder (/opt/pyNotify) and set the proper values for:
- gotify server url, and 
- gotify client token  (you may need to generate this in your Gotify server)

## Compilation
It's also possible to compile from source code in python (pyNotify.py).
I'm providing several bash scripts to build / compile with pyinstaller the python file:
- build.sh : just compiles the python file (pyNotify.py) generating the binary in a "dist" folder
- install.sh: just copies the resulting compiled files to /opt/pyNotify and creates the pyNotify.desktop file in your $HOME/.loca./share/applications
- build.and.install.sh: combination of both 
