# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Fernando Seoane <fseoane@hotmail.com>
pkgname=pyNotify
pkgver=0.4.r178.bac49f0
pkgrel=1
epoch=
pkgdesc="A Gnome (wayland) shell notifier for Gotify server."
arch=('x86_64')
url="https://github.com/fseoane/pyNotify.git"
license=('MIT')
groups=()
depends=('libappindicator-gtk3' 'gnome-shell-extension-appindicator')
makedepends=('git' 'python3' 'python-pip' 'python-virtualenv')
checkdepends=()
optdepends=()
provides=(pyNotify)
conflicts=(pyNotify)
replaces=(pyNotify)
backup=()
options=()
install=
changelog=
source=("git+$url")
noextract=()
md5sums=('SKIP')
validpgpkeys=()

pkgver() {
	cd "${_pkgname}"
	printf "0.4.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

prepare() {
	cd "$pkgname"
	echo "$pkgver" > pyNotify.ver
}

build() {
	cd "$pkgname"
	#sh build.Arch.sh
	mkdir .env 
	python -m venv .env
	source .env/bin/activate

	sudo -S pacman -S libappindicator-gtk3

	python  -m pip install --upgrade pip # setuptools wheel

	python -m pip uninstall gotify
	python -m pip uninstall gotify[stream]
	python -m pip uninstall pyinstaller
	python -m pip uninstall pycairo
	python -m pip uninstall pygame
	python -m pip uninstall pygobject
	python -m pip uninstall asyncio
	python -m pip uninstall pystray
	python -m pip uninstall pillow
	python -m pip uninstall websockets
	python -m pip uninstall psutil

	python -m pip cache purge

	#python -m pip install gotify
	python -m pip install gotify[stream]
	python -m pip install pyinstaller
	#python -m pip install pycairo
	python -m pip install pygame
	python -m pip install pygobject
	python -m pip install asyncio
	python -m pip install pystray
	python -m pip install pillow
	#python -m pip install websockets
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
}

# check() {
# 	cd "$pkgname-$pkgver"
# 	make -k check
# }

package() {
	cd "$pkgname"
	sudo mkdir -p /opt/${pkgname}
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/dist/${pkgname} /opt/${pkgname}/${pkgname}
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/${pkgname}.desktop /opt/${pkgname}/${pkgname}.desktop
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/*.ogg /opt/${pkgname}/
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/*.png /opt/${pkgname}/
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/*.svg /opt/${pkgname}/
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/${pkgname}.ver /opt/${pkgname}/${pkgname}.ver
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/${pkgname}.conf /opt/${pkgname}/${pkgname}.conf.default

	desktop-file-install --dir=$HOME/.local/share/applications /opt/${pkgname}/${pkgname}.desktop
	sudo install -Dm644 LICENSE "/usr/share/licenses/${pkgname}/LICENSE"
    sudo install -Dm644 README.md "/usr/share/doc/${pkgname}/README.md"


}
