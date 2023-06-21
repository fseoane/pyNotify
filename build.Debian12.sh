sudo -S pacman -S libappindicator-gtk3

mkdir .env 
python3 -m venv .env
source .env/bin/activate

python3  -m pip install --upgrade pip setuptools wheel

python3 -m pip install gotify
python3 -m pip install gotify[stream]
#python3 -m pip install playsound
python3 -m pip install pyinstaller
python3 -m pip install pycairo
python3 -m pip install pygame
python3 -m pip install pygobject
python3 -m pip install asyncio
python3 -m pip install pystray
python3 -m pip install pillow
python3 -m pip install websockets
python3 -m pip install psutil

pyinstaller --onefile --windowed pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env