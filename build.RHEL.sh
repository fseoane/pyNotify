sudo dnf install --assumeyes libappindicator-gtk3
sudo dnf install --assumeyes cairo-devel pkg-config python3-devel
sudo dnf install --assumeyes gobject-introspection-devel 
sudo dnf install --assumeyes cairo-gobject-devel 
mkdir .env 
python -m venv .env
source .env/bin/activate

python -m pip install --upgrade gotify
python -m pip install --upgrade gotify[stream]
#python -m pip install --use-pep517 playsound
python -m pip install --upgrade playsound
python -m pip install --upgrade pyinstaller
python -m pip install --upgrade pycairo
python -m pip install --upgrade pygobject
python -m pip install --upgrade pystray
python -m pip install --upgrade pillow
python -m pip install --upgrade websockets
python -m pip install --upgrade asyncio
python -m pip install --upgrade psutil

pyinstaller --onefile --windowed pyNotify.py

cp notification.ogg dist
cp notification.svg dist
cp notification.png dist
cp pyNotify.desktop dist
cp install.binaries.sh dist/install.sh
cp pyNotify.conf dist/pyNotify.conf

deactivate
rm -rf .env