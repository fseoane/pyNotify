
killall pyNotify

sudo mkdir -p /opt/pyNotify
sudo cp dist/*  /opt/pyNotify/
cp /opt/pyNotify/pyNotify.desktop ~/.local/share/applications
sudo chmod -R 755 /opt/pyNotify
sudo chown -R root:users /opt/pyNotify

echo "ATTENTION:"
echo "Please configure /opt/pyNotify/pyNotify.conf with the proper values¨
