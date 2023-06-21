
killall pyNotify

sudo mkdir -p /opt/pyNotify
sudo cp pyNotify /opt/pyNotify/
sudo cp pyNotify.desktop /opt/pyNotify/
sudo cp notification.* /opt/pyNotify/

read -r -p "Install default configuration file (pyNotify.conf)? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
        sudo cp pyNotify.conf /opt/pyNotify/
else
		echo "Skipped"
fi

sudo chmod -R 755 /opt/pyNotify
sudo chown -R root:users /opt/pyNotify
desktop-file-install --dir=$HOME/.local/share/applications /opt/pyNotify/pyNotify.desktop

echo "ATENTION:"
echo "Please configure /opt/pyNotify/pyNotify.conf with the proper values"