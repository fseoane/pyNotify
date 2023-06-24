#!/bin/bash

echo "0.6.r$(git rev-list --count HEAD).$(git rev-parse --short HEAD)" > pyNotify.ver

mkdir -p .env 
python -m venv .env
source .env/bin/activate

python -m pip install -r requirements.req

pyinstaller --onefile --windowed --icon notification.svg --upx-dir /usr/bin/ pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.ver dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env
