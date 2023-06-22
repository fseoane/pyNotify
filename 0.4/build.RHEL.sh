mkdir -p .env 
python3.11  -m venv .env
source .env/bin/activate

sudo dnf install --assumeyes libappindicator-gtk3
sudo dnf install --assumeyes pkg-config python3.11-devel

python3.11  -m pip install --upgrade pip setuptools wheel

python3.11  -m pip install --upgrade gotify
python3.11  -m pip install --upgrade gotify[stream]
python3.11  -m pip install --upgrade pygame
python3.11  -m pip install --upgrade pyinstaller
python3.11  -m pip install --upgrade pycairo
python3.11  -m pip install --upgrade pygobject
python3.11  -m pip install --upgrade pystray
python3.11  -m pip install --upgrade pillow
python3.11  -m pip install --upgrade websockets
python3.11  -m pip install --upgrade async
python3.11  -m pip install --upgrade asyncio
python3.11  -m pip install --upgrade psutil

pyinstaller --onefile --windowed pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env