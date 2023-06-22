# pyNotify
A gnome (wayland) notifier for Gotify server.

Gotify server is open source software for notifications that can be deployed on-prem (self-hosted). 
It provides web based service, API,  and also mobile application, but I was missing a working gnome tray notification app for receiving those notifications directly in my gnome desktop (wayland), so I build this.

## 1.Requirements for running the binaries from the release package (precompiled)
Built on Python 3.11

It also requires Ayatana AppIndicator3 and Gnome shell extension "AppIndicator and KStatusNotifierItem Support".

To install support for Ayatana AppIndicator3 library:

- Arch :
      sudo pacman -S libappindicator-gtk3
  
- Debian 12 :
      sudo apt install libappindicator3-dev
      sudo apt install libcairo2-dev libjpeg-dev libgif-dev
      sudo apt install libgirepository1.0-dev
 
- RedHat 9/Fedora :
      sudo dnf install libappindicator-gtk3
      sudo dnf install pkg-config python3.11-devel

The Gnome shell extension "AppIndicator and KStatusNotifierItem Support" can be installed from : https://extensions.gnome.org/extension/615/appindicator-support/

### 1.1.Installing the release package (precompiled)
Download the release package and copy itś contents to /opt/pyNotify. 
This release package has a binary already compiled and ready to execute on Linux.
The bash script (install.sh) inside the realease package will copy all the necessary files to /opt/pyNotify in one go.....

....just edit the file pyNotify.conf in that destination folder (/opt/pyNotify) and set the proper values for:
- gotify server url, and 
- gotify client token  (you may need to generate this in your Gotify server)

## 2.Building / Compiling
It's also possible to compile from source code in python (pyNotify.py).

I'm providing several bash scripts to build / compile with pyinstaller the python file:
- build.XXX.sh : just installs dependencies for XXX distro and compiles the python file (pyNotify.py) generating the binary in a "dist" folder
- install.sh: just copies the resulting compiled files to /opt/pyNotify and creates the pyNotify.desktop file in your $HOME/.loca./share/applications
- build.and.install.sh: combination of both
- install.binaries.sh: do not use this....itś meant to be copied into the dist folder to install the resulting compiled files to /opt/pyNotify

### 2.1.Dependencies for building / compiling
Please make sure you install these dependencies (along the previous ones) before building on your own (not using the build.XXX.sh provided)
- Any one/other
      python3.11
      python3.11 virtual environments (venv module)
      python3.11 pip

- Arch :
      sudo pacman -S python3
      sudo pacman -S python-virtualenv
  
- Debian 12 :
      sudo apt install python3.11-venv
      sudo apt install python3-pip
      sudo apt install virtualenv

- RedHat 9/Fedora :
      sudo dnf install python3.11-* (all packages) or just...
      sudo dnf install python3.11-venv
      sudo dnf install python3.11-pip

