# Maintainer: Redecorating
# Contributor: James Lambert (jamlam) <jamesl@mbert.onmicrosoft.com>
# Contributor: Aun-Ali Zaidi <admin@kodeit.net>
# Contributor: Jan Alexander Steffens (heftig) <jan.steffens@gmail.com>

pkgbase=linux-t2
pkgver=5.15.11
_srcname=linux-${pkgver}
pkgrel=2
pkgdesc='Linux kernel for T2 Macs'
_srctag=v${pkgver%.*}-${pkgver##*.}
url="https://git.archlinux.org/linux.git/log/?h=v$_srctag"
arch=(x86_64)
license=(GPL2)
makedepends=(
  bc kmod libelf pahole cpio perl tar xz 
  xmlto python-sphinx python-sphinx_rtd_theme graphviz imagemagick
  git
)
options=('!strip')

source=(
  https://www.kernel.org/pub/linux/kernel/v${pkgver//.*}.x/linux-${pkgver}.tar.xz
  https://www.kernel.org/pub/linux/kernel/v${pkgver//.*}.x/linux-${pkgver}.tar.sign
  config         # the main kernel config file

  # Arch Linux patches
  0001-ZEN-Add-sysctl-and-CONFIG-to-disallow-unprivileged-C.patch
  0002-HID-quirks-Add-Apple-Magic-Trackpad-2-to-hid_have_sp.patch

  # apple-bce, apple-ibridge
  apple-bce::git+https://github.com/t2linux/apple-bce-drv#commit=f93c6566f98b3c95677de8010f7445fa19f75091
  apple-ibridge::git+https://github.com/t2linux/apple-ib-drv#commit=d8411ad1d87db8491e53887e36c3d37f445203eb
  1001-Put-apple-bce-and-apple-ibridge-in-drivers-staging.patch
  1002-add-modalias-to-apple-bce.patch

  # Hack for AMD DC eDP link rate bug
  2001-drm-amd-display-Force-link_rate-as-LINK_RATE_RBR2-fo.patch

  # Apple SMC ACPI support
  3001-applesmc-convert-static-structures-to-drvdata.patch
  3002-applesmc-make-io-port-base-addr-dynamic.patch
  3003-applesmc-switch-to-acpi_device-from-platform.patch
  3004-applesmc-key-interface-wrappers.patch
  3005-applesmc-basic-mmio-interface-implementation.patch
  3006-applesmc-fan-support-on-T2-Macs.patch

  # T2 USB Keyboard/Touchpad support
  4001-HID-apple-Add-support-for-keyboard-backlight-on-supp.patch
  4002-HID-apple-Add-support-for-MacbookAir8-1-keyboard-tra.patch
  4003-HID-apple-Add-support-for-MacBookPro15-2-keyboard-tr.patch
  4004-HID-apple-Add-support-for-MacBookPro15-1-keyboard-tr.patch
  4005-HID-apple-Add-support-for-MacBookPro15-4-keyboard-tr.patch
  4006-HID-apple-Add-support-for-MacBookPro16-2-keyboard-tr.patch
  4007-HID-apple-Add-support-for-MacBookPro16-3-keyboard-tr.patch
  4008-HID-apple-Add-support-for-MacBookAir9-1-keyboard-tra.patch
  4009-HID-apple-Add-support-for-MacBookPro16-1-keyboard-tr.patch
  
  # UVC Camera support
  6001-media-uvcvideo-Add-support-for-Apple-T2-attached-iSi.patch

  # Hack for i915 overscan issues
  7001-drm-i915-fbdev-Discard-BIOS-framebuffers-exceeding-h.patch

  # Broadcom WIFI device support
  8001-brcmfmac-pcie-Declare-missing-firmware-files-in-pcie.patch
  8002-brcmfmac-firmware-Support-having-multiple-alt-paths.patch
  8003-brcmfmac-firmware-Handle-per-board-clm_blob-files.patch
  8004-brcmfmac-pcie-sdio-usb-Get-CLM-blob-via-standard-fir.patch
  8005-brcmfmac-firmware-Support-passing-in-multiple-board_.patch
  8006-brcmfmac-pcie-Read-Apple-OTP-information.patch
  8007-brcmfmac-of-Fetch-Apple-properties.patch
  8008-brcmfmac-pcie-Perform-firmware-selection-for-Apple-p.patch
  8009-brcmfmac-firmware-Allow-platform-to-override-macaddr.patch
  8010-brcmfmac-msgbuf-Increase-RX-ring-sizes-to-1024.patch
  8011-brcmfmac-pcie-Fix-crashes-due-to-early-IRQs.patch
  8012-brcmfmac-pcie-Support-PCIe-core-revisions-64.patch
  8013-brcmfmac-pcie-Add-IDs-properties-for-BCM4378.patch
  8014-ACPI-property-Support-strings-in-Apple-_DSM-props.patch
  8015-brcmfmac-acpi-Add-support-for-fetching-Apple-ACPI-pr.patch
  8016-brcmfmac-pcie-Provide-a-buffer-of-random-bytes-to-th.patch
  8017-brcmfmac-pcie-Add-IDs-properties-for-BCM4355.patch
  8018-brcmfmac-pcie-Add-IDs-properties-for-BCM4377.patch
  8019-brcmfmac-pcie-Perform-correct-BCM4364-firmware-selec.patch
  8020-brcmfmac-chip-Only-disable-D11-cores-handle-an-arbit.patch
  8021-brcmfmac-chip-Handle-1024-unit-sizes-for-TCM-blocks.patch
  8022-brcmfmac-cfg80211-Add-support-for-scan-params-v2.patch
  8023-brcmfmac-feature-Add-support-for-setting-feats-based.patch
  8024-brcmfmac-cfg80211-Add-support-for-PMKID_V3-operation.patch
  8025-brcmfmac-cfg80211-Pass-the-PMK-in-binary-instead-of-.patch
  8026-brcmfmac-pcie-Add-IDs-properties-for-BCM4387.patch
  8027-brcmfmac-pcie-Replace-brcmf_pcie_copy_mem_todev-with.patch
  8028-brcmfmac-pcie-Read-the-console-on-init-and-shutdown.patch
  8029-brcmfmac-pcie-Release-firmwares-in-the-brcmf_pcie_se.patch

  # Broadcom BT device support
  9001-bluetooth-add-disable-read-tx-power-quirk.patch
  9002-add-bluetooth-support-for-16,2.patch
  9003-mfd-intel-lpss-Fix-too-early-PM-enablement-in-the-AC.patch

  
)

validpgpkeys=(
  'ABAF11C65A2970B130ABE3C479BE3E4300411886'  # Linus Torvalds
  '647F28654894E3BD457199BE38DBBDC86092693E'  # Greg Kroah-Hartman
)

export KBUILD_BUILD_HOST=archlinux
export KBUILD_BUILD_USER=$pkgbase
export KBUILD_BUILD_TIMESTAMP="$(date -Ru${SOURCE_DATE_EPOCH:+d @$SOURCE_DATE_EPOCH})"

prepare() {
  cd $_srcname

  echo "Setting version..."
  scripts/setlocalversion --save-scmversion
  echo "-$pkgrel" > localversion.10-pkgrel
  echo "${pkgbase#linux}" > localversion.20-pkgname

  for i in apple-bce apple-ibridge; do
    echo "Copying $i in to drivers/staging..."
	# no need to copy .git/
	mkdir drivers/staging/$i
    cp -r $srcdir/$i/* drivers/staging/$i/
  done

  local src
  for src in "${source[@]}"; do
    src="${src%%::*}"
    src="${src##*/}"
    [[ $src = *.patch ]] || continue
    echo "Applying patch $src..."
    patch -Np1 < "../$src"
  done

  echo "Setting config..."
  cp ../config .config
  make olddefconfig

  make -s kernelrelease > version
  echo "Prepared $pkgbase version $(<version)"
}

build() {
  cd $_srcname
  make all
  make htmldocs
}

_package() {
  pkgdesc="The $pkgdesc kernel and modules"
  depends=(coreutils kmod initramfs)
  optdepends=('crda: to set the correct wireless channels of your country'
              'linux-firmware: firmware images needed for some devices')
  provides=(VIRTUALBOX-GUEST-MODULES WIREGUARD-MODULE)
  replaces=(virtualbox-guest-modules-arch wireguard-arch)
  provides=("linux=$pkgver")

  cd $_srcname
  local kernver="$(<version)"
  local modulesdir="$pkgdir/usr/lib/modules/$kernver"

  echo "Installing boot image..."
  # systemd expects to find the kernel here to allow hibernation
  # https://github.com/systemd/systemd/commit/edda44605f06a41fb86b7ab8128dcf99161d2344
  install -Dm644 "$(make -s image_name)" "$modulesdir/vmlinuz"

  # Used by mkinitcpio to name the kernel
  echo "$pkgbase" | install -Dm644 /dev/stdin "$modulesdir/pkgbase"

  echo "Installing modules..."
  make INSTALL_MOD_PATH="$pkgdir/usr" INSTALL_MOD_STRIP=1 modules_install

  # remove build and source links
  rm "$modulesdir"/{source,build}
}

_package-headers() {
  pkgdesc="Headers and scripts for building modules for the $pkgdesc kernel"
  provides=("linux-headers=$pkgver")

  cd $_srcname
  local builddir="$pkgdir/usr/lib/modules/$(<version)/build"

  echo "Installing build files..."
  install -Dt "$builddir" -m644 .config Makefile Module.symvers System.map \
    localversion.* version vmlinux
  install -Dt "$builddir/kernel" -m644 kernel/Makefile
  install -Dt "$builddir/arch/x86" -m644 arch/x86/Makefile
  cp -t "$builddir" -a scripts

  # add objtool for external module building and enabled VALIDATION_STACK option
  install -Dt "$builddir/tools/objtool" tools/objtool/objtool

  # add xfs and shmem for aufs building
  mkdir -p "$builddir"/{fs/xfs,mm}

  echo "Installing headers..."
  cp -t "$builddir" -a include
  cp -t "$builddir/arch/x86" -a arch/x86/include
  install -Dt "$builddir/arch/x86/kernel" -m644 arch/x86/kernel/asm-offsets.s

  install -Dt "$builddir/drivers/md" -m644 drivers/md/*.h
  install -Dt "$builddir/net/mac80211" -m644 net/mac80211/*.h

  # http://bugs.archlinux.org/task/13146
  install -Dt "$builddir/drivers/media/i2c" -m644 drivers/media/i2c/msp3400-driver.h

  # http://bugs.archlinux.org/task/20402
  install -Dt "$builddir/drivers/media/usb/dvb-usb" -m644 drivers/media/usb/dvb-usb/*.h
  install -Dt "$builddir/drivers/media/dvb-frontends" -m644 drivers/media/dvb-frontends/*.h
  install -Dt "$builddir/drivers/media/tuners" -m644 drivers/media/tuners/*.h

  echo "Installing KConfig files..."
  find . -name 'Kconfig*' -exec install -Dm644 {} "$builddir/{}" \;

  echo "Removing unneeded architectures..."
  local arch
  for arch in "$builddir"/arch/*/; do
    [[ $arch = */x86/ ]] && continue
    echo "Removing $(basename "$arch")"
    rm -r "$arch"
  done

  echo "Removing documentation..."
  rm -r "$builddir/Documentation"

  echo "Removing broken symlinks..."
  find -L "$builddir" -type l -printf 'Removing %P\n' -delete

  echo "Removing loose objects..."
  find "$builddir" -type f -name '*.o' -printf 'Removing %P\n' -delete

  echo "Stripping build tools..."
  local file
  while read -rd '' file; do
    case "$(file -bi "$file")" in
      application/x-sharedlib\;*)      # Libraries (.so)
        strip -v $STRIP_SHARED "$file" ;;
      application/x-archive\;*)        # Libraries (.a)
        strip -v $STRIP_STATIC "$file" ;;
      application/x-executable\;*)     # Binaries
        strip -v $STRIP_BINARIES "$file" ;;
      application/x-pie-executable\;*) # Relocatable binaries
        strip -v $STRIP_SHARED "$file" ;;
    esac
  done < <(find "$builddir" -type f -perm -u+x ! -name vmlinux -print0)

  echo "Stripping vmlinux..."
  strip -v $STRIP_STATIC "$builddir/vmlinux"

  echo "Adding symlink..."
  mkdir -p "$pkgdir/usr/src"
  ln -sr "$builddir" "$pkgdir/usr/src/$pkgbase"
}

_package-docs() {
  pkgdesc="Documentation for the $pkgdesc kernel"

  cd $_srcname
  local builddir="$pkgdir/usr/lib/modules/$(<version)/build"

  echo "Installing documentation..."
  local src dst
  while read -rd '' src; do
    dst="${src#Documentation/}"
    dst="$builddir/Documentation/${dst#output/}"
    install -Dm644 "$src" "$dst"
  done < <(find Documentation -name '.*' -prune -o ! -type d -print0)

  echo "Adding symlink..."
  mkdir -p "$pkgdir/usr/share/doc"
  ln -sr "$builddir/Documentation" "$pkgdir/usr/share/doc/$pkgbase"
}

pkgname=("$pkgbase" "$pkgbase-headers" "$pkgbase-docs")
for _p in "${pkgname[@]}"; do
  eval "package_$_p() {
    $(declare -f "_package${_p#$pkgbase}")
    _package${_p#$pkgbase}
  }"
done

sha256sums=('c1178b7e7e12d91292e670191268e3fe9a3563faf899eef43e468577e973a1ce'
            'SKIP'
            '324a9d46c2338806a0c3ce0880c8d5e85c2ef30d342af3dc96f87b54fae7a586'
            '6b4da532421cac5600d09c0c52742aa52d848af098f7853abe60c02e9d0a3752'
            '2184069ab00ef43d9674756e9b7a56d15188bc4494d34425f04ddc779c52acd8'
            'SKIP'
            'SKIP'
            'b7c987889d92a48d638d5258842b10f6c856e57f29ad23475aa507c7b4ad5710'
            '0e371fe1efd1ec422f89439a2befb5a0c3dd28c9e60780f55493d9699c6ebc0e'
            '786dfc22e4c6ece883e7dedd0ba3f6c14018584df95450b2cb78f3da8b01f7cb'
            '7366a08383900a09f8e742b1e4f0a02e0839a385e68e70a89d1815c197df3300'
            '8d8401a99a9dfbc41aa2dc5b6a409a19860b1b918465e19de4a4ff18de075ea3'
            '08d165106fe35b68a7b48f216566951a5db0baac19098c015bcc81c5fcba678d'
            '459906cab172df9f6712a4168e7a5d529f85b2bb58a068f2d44746df14a6d27a'
            '2827dab6eeb2d2a08034938024f902846b5813e967a0ea253dc1ea88315da383'
            '398dec7d54c6122ae2263cd5a6d52353800a1a60fd85e52427c372ea9974a625'
            '11565cff9c6a7db8846dc7d5930419045e9527863b8df5979a7465006211bd16'
            '83f4be6849ba4d5f9fad647ad2eb78bf6409ee98a40ac62e8a5b80496233d70a'
            '44bd3643b2b22fedc59d79511199f30ce6759fa0acdd9a66262a53c5e046da6b'
            'eb04a492197783643b3e72b1d0cf0e856290381997bd165a14fbc63ac1489c25'
            '69d56d42473526f7dbd4fb18c5e1baafe4e6d32995b2506bd48ff981c53b5385'
            '1deeacae1875cf9075b858a8bfb2463ebc531c9030b7c2ab46bbb8e4c3b974db'
            '40eff5e88bb30c51c6b97e85c2e7b8dec5f97916f768e6c07618d9c5afe68574'
            'cac035fe07663a319185c644c5b39b34bef89ada348881fa4a02d15290260445'
            '9dfa9f02d17c5cd9620fa2c1d43ca967b81b6a56d33c2bafae14e0c64e498baa'
            '9640178d6251686c980c30fc528b3d70beac6ce8246bf433506a3f843808326c'
            '90a6012cdd8a64ede8e0bbaf7331960bd68f628e0973b65459188eb1ccb5b829'
            '23a44991bcd6254ff91ab259900bb7decad16efc5b87498c93fcd9bb86fe561a'
            '0d0c3b2a5e30b29d6c93a760f9b4fab1dd30a9561be56ecd43c7471e674aee26'
            '9bf9dd0d978a649c7e0437ac8f42a11f09af4917fe1968dc26223692137fc517'
            'c4966acab11e2e9f61132d8740371b404317d49ba86e899e01faa6896736675e'
            '53ad3c9fae3472c9f572bb485190c6d865656435742584a83f411c3f6eaebf49'
            '7616371062addcc256c9217c65b92da59e5f16b35845cd3f7d537bf2bcde08bd'
            '0011ae2df9e8cd87adb46f7c0a0edfe83bbbb845cc141db304be63cb03118f26'
            '4f36a11f3545c4db77187395b10e078525a4c494fa6a0f58bc85bdb53403afda'
            '4f7b22bc363fab93199e77a5713ea51b6a32d1087c0efbc8b36cb9d1ce3df620'
            'e2b483966f138e9112027e47280a5045c80694bc1b8f132ebfec271b9155bbe2'
            'e71a275dbcfb7f394b946c748f3317fffe7a6d6df897f766b537fe0ba7cd1e0d'
            '8770b56adb15004e624a98b9675e496c2ac662744f899f058a18b16868bd04f6'
            '3badfb3ea7c17ce948524a22284370f0739c59e62ea529c869329243e66682ca'
            'c25d935ed2e21308389aac775d029c32eecc6a8fdef1dc3df4c745c0d46981ea'
            '96b954987bcbe7ea0ba24943c00570570adfb74e2ba7e1f0df3c4074d0f4d112'
            '5c89f30332ce30e010c1e6dcfcef41bb7ce3411acc147b6b00925c24cc0f9086'
            '08d4b7b71264b1d62c58eb5535c76b44d087654e0895b0c543972c2c264e9cc7'
            '54fa470bc8b1b3a449e19860a11cd9ee5dfdf297a05f90dc0029a4e30ee0de43'
            'e5e2cdd0140e93e1f599f37ba0380ce1f51646b35cfccdb7a5a0e02a7eb7afdb'
            '4b1d72c3d402e9135810dde26bcfd41cee3c988c4f5644eedf8d5254376dc329'
            'b256ec4d4057019ede92fff228a959a8be99a9130078b7cda5265a5f1e3a000e'
            '0c30315c95c27e1fb64e0af972e8ec27ffd3333869ffa7ab5cefb8cbc7abce38'
            '5453c12bb8084e19c5e8e627084a644663b209f7812fd6149dee0c5e18f7f577'
            'a9497ecbb19e3c24eb057d2a5c57ddc91dd78be7f370ea0965e7a93316f11ade'
            '143e7c874feb714f0075969662a245ecacf60f243ed6c7b3bb1030c00b605f94'
            '1745213ecf75126cd77a98324545995faef0477e9df35a76ae02a3bb8707ab3f'
            'ba5660c533d3d91bcb2f4452e7e3125f594457567478e87fba58c1296c58c096'
            '1096b078a9870ffc528a4001b534dd5bc3e03b24e33225d930b4f5be2efadeb8'
            '5980bbc0702eafebcbbe80c53d39f985422247020b811e44c333fe047d1ab779'
            '31e414978a947bdb71f27ed364c4da73b81fcf1921250cb69ee1bcf2bbd25636'
            '5d36770f436b69e69633d060deb55a37b8b3871983068e95fb33d5a195f00574'
            '3bffb2bb84800453ba05676293de9b0b1619d0c19b6295e803f0d9c3a07be23a')
