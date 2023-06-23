#!/bin/bash

sudo apt install python3.11-venv -y
sudo apt install python3-pip -y

mkdir -p .env 
python3.11 -m venv .env
source .env/bin/activate

sudo apt install virtualenv -y
sudo apt install libcairo2-dev libjpeg-dev libgif-dev -y
sudo apt install libgirepository1.0-dev -y
sudo apt install libappindicator3-dev -y

python3.11  -m pip install --upgrade pip setuptools wheel

python3.11 -m pip install gotify
python3.11 -m pip install gotify[stream]
python3.11 -m pip install pyinstaller
python3.11 -m pip install pycairo
python3.11 -m pip install pygame
python3.11 -m pip install pygobject
python3.11 -m pip install asyncio
python3.11 -m pip install pystray
python3.11 -m pip install pillow
python3.11 -m pip install websockets
python3.11 -m pip install psutil

pyinstaller --onefile --windowed pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env