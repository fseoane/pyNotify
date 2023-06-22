# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Fernando Seoane <fseoane@hotmail.com>
pkgname=pyNotify
pkgver=0.4
pkgrel=1
epoch=
pkgdesc="A Gnome (wayland) shell notifier for Gotify server."
arch=(x86_64 i686)
url="https://github.com/fseoane/pyNotify.git"
license=('MIT')
groups=()
depends=(libappindicator-gtk3 gnome-shell-extension-appindicator)
makedepends=(git python3 python-pip python-virtualenv)
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

# prepare() {
# 	cd "$pkgname-$pkgver"
# 	patch -p1 -i "$srcdir/pyNotify/$pkgver.patch"
# }

build() {
	cd "$pkgname"
	sh build.Arch.sh
}

# check() {
# 	cd "$pkgname-$pkgver"
# 	make -k check
# }

package() {
	cd "$pkgname"
	#killall $pkgname   # to allow the copy of new file sin case itś already runing
	mkdir -p /opt/${pkgname}
	#sudo chown -R root:users /opt/${pkgname}

	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/dist/${pkgname} /opt/${pkgname}/${pkgname}
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/${pkgname}.desktop /opt/${pkgname}/${pkgname}.desktop
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/*.ogg /opt/${pkgname}/
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/*.png /opt/${pkgname}/
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/*.svg /opt/${pkgname}/
	sudo install -Dm755 --owner=root --group=users ${srcdir}/${pkgname}/${pkgname}.conf /opt/${pkgname}/${pkgname}.conf.default


	# sudo cp ${srcdir}/${pkgname}/dist/${pkgname} /opt/${pkgname}/${pkgname}
	# sudo cp ${srcdir}/${pkgname}/${pkgname}.desktop /opt/${pkgname}/${pkgname}.desktop
	# sudo cp ${srcdir}/${pkgname}/*.ogg /opt/${pkgname}/
	# sudo cp ${srcdir}/${pkgname}/*.png /opt/${pkgname}/
	# sudo cp ${srcdir}/${pkgname}/*.svg /opt/${pkgname}/
	# sudo cp ${srcdir}/${pkgname}/${pkgname}.conf /opt/${pkgname}/${pkgname}.conf.default
	# chmod -R 755 /opt/${pkgname}
	# chown -R root:users /opt/${pkgname}
	desktop-file-install --dir=$HOME/.local/share/applications /opt/${pkgname}/${pkgname}.desktop
	sudo install -Dm644 LICENSE "/usr/share/licenses/${pkgname}/LICENSE"
    sudo install -Dm644 README.md "/usr/share/doc/${pkgname}/README.md"

}
