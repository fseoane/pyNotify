#!/bin/bash

echo "0.5.r$(git rev-list --count HEAD).$(git rev-parse --short HEAD)" > pyNotify.ver


sudo dnf install --assumeyes libappindicator-gtk3
sudo dnf install --assumeyes pkg-config python3.11-devel

mkdir -p .env 
python3.11  -m venv .env
source .env/bin/activate

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
