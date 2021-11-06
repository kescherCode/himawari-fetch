# Maintainer: Jeremy Kescher <jeremy@kescher.at>

pkgname=himawari-fetch
_srcname=himawari_fetch
pkgver=1.0.0
pkgrel=1
pkgdesc="Set near-realtime picture of Earth into a directory"
arch=('any')
url="https://github.com/kescherCode/${_srcname}"
license=('MIT')
depends=('python-requests' 'python-pillow')
makedepends=('python-setuptools' 'python-wheel')
source=("${_srcname}-${pkgver}.tar.gz::https://github.com/kescherCode/${_srcname}/archive/v${pkgver}.tar.gz")
sha256sums=('SKIP')

build() {
    cd "${_srcname}-${pkgver}"
    python setup.py build
}

package() {
    cd "${_srcname}-${pkgver}"
    python setup.py install --root="${pkgdir}" --optimize=1 --skip-build
    install -Dm0644 systemd/${pkgname}.service "${pkgdir}/usr/lib/systemd/system/${pkgname}.service"
    install -Dm0644 systemd/${pkgname}.timer "${pkgdir}/usr/lib/systemd/system/${pkgname}.timer"
    install -Dm0644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    install -d "${pkgdir}/var/lib/himawari-fetch"
}
