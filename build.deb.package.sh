echo "WARNING:"
echo "This script only runs on debian ande derivatives"

cp dist/pyNotify DEB.pyNotify.deb/opt/pyNotify/
cp dist/pyNotify.ver DEB.pyNotify.deb/opt/pyNotify/
cp dist/pyNotify.desktop DEB.pyNotify.deb/opt/pyNotify/
cp dist/notification.* DEB.pyNotify.deb/opt/pyNotify/
cp dist/pyNotify.conf DEB.pyNotify.deb/opt/pyNotify/
cp dist/pyNotify.conf DEB.pyNotify.deb/etc/

dpkg-deb --build DEB.pyNotify.deb