
killall pyNotify

sudo mkdir -p /opt/pyNotify
sudo cp pyNotify /opt/pyNotify/
sudo cp pyNotify.ver /opt/pyNotify/
sudo cp pyNotify.desktop /opt/pyNotify/
sudo cp notification.* /opt/pyNotify/

read -r -p "Install default configuration file (pyNotify.conf)? [y/N] " response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
	sudo cp pyNotify.conf /opt/pyNotify/
	sudo cp pyNotify.conf /etc/
	echo "ATENTION:"
	echo "Please configure file /opt/pyNotify/pyNotify.conf with your proper values"
else
	echo "Skipped installing default configuration file"
fi

sudo chmod -R 755 /opt/pyNotify
sudo chown -R root:users /opt/pyNotify
sudo desktop-file-install --dir=$HOME/.local/share/applications /opt/pyNotify/pyNotify.desktop

echo "Done."
