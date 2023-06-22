#!/bin/bash

mkdir .env 
python -m venv .env
source .env/bin/activate

sudo -S pacman -S libappindicator-gtk3

python  -m pip install --upgrade pip setuptools wheel

python -m pip uninstall gotify
python -m pip uninstall gotify[stream]
python -m pip uninstall pyinstaller
python -m pip uninstall pycairo
python -m pip uninstall pygame
python -m pip uninstall pygobject
python -m pip uninstall asyncio
python -m pip uninstall pystray
python -m pip uninstall pillow
python -m pip uninstall websockets
python -m pip uninstall psutil

python -m pip install gotify
python -m pip install gotify[stream]
python -m pip install pyinstaller
python -m pip install pycairo
python -m pip install pygame
python -m pip install pygobject
python -m pip install asyncio
python -m pip install pystray
python -m pip install pillow
python -m pip install websockets
python -m pip install psutil

pyinstaller --onefile --windowed pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env