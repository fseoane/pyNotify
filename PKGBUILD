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
	killall $pkgname   # to allow the copy of new file sin case itś already runing
	mkdir -p /opt/${pkgname}
	make PREFIX=/opt DESTDIR="${pkgdir}" install
	#cp ${pkgname}/dist/${pkgname} /opt/${pkgname}/${pkgname}
	sudo cp ${pkgname}.desktop /opt/${pkgname}/${pkgname}.desktop
	sudo cp *.ogg /opt/${pkgname}/
	sudo cp *.png /opt/${pkgname}/
	sudo cp *.svg /opt/${pkgname}/
	sudo cp *.conf /opt/${pkgname}/${pkgname}.conf.default
	chmod -R 755 ${pkgdir}/opt/${pkgname}
	chown -R root:users ${pkgdir}/opt/${pkgname}
	desktop-file-install --dir=$HOME/.local/share/applications /opt/${pkgname}/${pkgname}.desktop
	install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"

}
