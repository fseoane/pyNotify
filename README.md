# pyNotify
A gnome (wayland) notifier for Gotify server.

Gotify server is open source software for notifications that can be deployed on-prem (self-hosted). 
It provides web based service, API,  and also mobile application, but I was missing a working gnome tray notification app for receiving those notifications directly in my gnome desktop (wayland), so I build this.

## Requirements
Built on Python 3.11

It also requires Ayatana AppIndicator3 and Gnome-desktop extension "AppIndicator and KStatusNotifierItem Support".

To install support for Ayatana AppIndicator3 library:
- Arch  (OK - TESTED):
  sudo pacman -S libappindicator-gtk3
- Debian (NOT TESTED):
  sudo apt install gir1.2-appindicator3-0.1
- Fedora (NOT TESTED):
  sudo dnf install libappindicator-gtk3 cairo-devel pkg-config python3-devel
  gobject-introspection-devel cairo-gobject-devel python3-websockets python3-aiohttp

The Gnome-desktop extension "AppIndicator and KStatusNotifierItem Support" can be installed from : https://extensions.gnome.org/extension/615/appindicator-support/
  

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
