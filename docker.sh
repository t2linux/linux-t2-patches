#!/bin/bash

if ! [ -e PKGBUILD ]
then echo "No PKGBUILD, go learn github ci"
	exit 1
fi

docker pull archlinux

docker run -t -v $PWD:/build archlinux /bin/bash -c \
	"cd /build
	useradd builduser -m
	passwd -d builduser
	pacman -Syu --noconfirm --needed sudo base-devel
	printf 'builduser ALL=(ALL) ALL\n' | tee -a /etc/sudoers
	chown -R builduser:builduser ./
	sudo -u builduser gpg --keyserver hkp://keys.gnupg.net:80 --recv-keys 38DBBDC86092693E
	sudo -u builduser bash -c 'export MAKEFLAGS=j\$(nproc) && makepkg -s --noconfirm'
	ls -lah *.pkg.tar.*"
	# from https://github.com/aunali1/linux-mbp-arch/blob/master/.drone.yml
