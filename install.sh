
killall pyNotify

sudo mkdir -p /opt/pyNotify
sudo cp dist/*  /opt/pyNotify/
cp /opt/pyNotify/pyNotify.desktop ~/.local/share/applications
desktop-file-install --dir=$HOME/.local/share/applications /opt/pyNotify/pyNotify.desktop
sudo chmod -R 755 /opt/pyNotify
sudo chown -R root:users /opt/pyNotify

echo "ATENTION:"
echo "Please configure /opt/pyNotify/pyNotify.conf with the proper values¨
