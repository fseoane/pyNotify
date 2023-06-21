sudo -S pacman -S libappindicator-gtk3

mkdir .env 
python -m venv .env
source .env/bin/activate

python -m pip install gotify
python -m pip install gotify[stream]
python -m pip install playsound
python -m pip install pyinstaller
python -m pip install pycairo
python -m pip install pygobject
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