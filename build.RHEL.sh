sudo dnf install --assumeyes libappindicator-gtk3
sudo dnf install --assumeyes cairo-devel pkg-config python3-devel
sudo dnf install --assumeyes gobject-introspection-devel 
sudo dnf install --assumeyes cairo-gobject-devel 
sudo dnf install --assumeyes python3-websockets python3-aiohttp

mkdir -p .env 
python3.11  -m venv .env
source .env/bin/activate

python3.11  -m pip install --upgrade pip setuptools wheel

python3.11  -m pip install --upgrade gotify
python3.11  -m pip install --upgrade gotify[stream]
#python3.11  -m pip install --use-pep517 playsound
#python3.11  -m pip install --upgrade playsound
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

pyinstaller --onefile --windowed pyNotify.py > build.RHEL.pyinstaller.log

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
#rm -rf .env