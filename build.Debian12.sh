#!/bin/bash

echo "0.5.r$(git rev-list --count HEAD).$(git rev-parse --short HEAD)" > pyNotify.ver

sudo apt install python3.11-venv -y
sudo apt install python3-pip -y
# sudo apt install virtualenv -y

sudo apt install libcairo2-dev libjpeg-dev libgif-dev -y
sudo apt install libgirepository1.0-dev -y
sudo apt install libappindicator3-dev -y

mkdir -p .env 
python3.11 -m venv .env
. ./.env/bin/activate

python3.11 -m pip install -r requirements.req

pyinstaller --onefile --windowed pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.ver dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env
