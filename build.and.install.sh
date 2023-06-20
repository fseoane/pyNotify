mkdir .env 
python -m venv .env
source .env/bin/activate

#python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel

python -m pip install gotify
python -m pip install gotify[stream]
python -m pip install playsound
python -m pip install pyinstaller
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
cp pyNotify.conf dist/pyNotify.conf

sudo mkdir -p /opt/pyNotify
sudo cp dist/*  /opt/pyNotify/
cp /opt/pyNotify/pyNotify.desktop ~/.local/share/applications
sudo chmod -R 755 /opt/pyNotify
sudo chown -R root:users /opt/pyNotify

echo "ATTENTION:"
echo "Please configure /opt/pyNotify/pyNotify.conf with the proper values¨

deactivate
rm -rf .env