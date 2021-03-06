ADDON = se_nauman_packages se_nauman_crypto
ADDONDIR = /usr/share/anaconda/addons/
PICS = pics/*
PICSDIR = /usr/share/anaconda/pixmaps/
OUTFILE = /tmp/anaconda_addon.img
DESTDIR := $(if $(DESTDIR),$(DESTDIR),)

all:
	@echo "usage:"
	@echo "   make install"
	@echo "   make uninstall"
	@echo "   make package"
	@echo "   make package DESTDIR=`mktemp -d`"

install:
	mkdir -p $(DESTDIR)$(ADDONDIR)
	
	# Addon
	cp -rv $(ADDON) $(DESTDIR)$(ADDONDIR)
	
	# Logo / Background	
	mkdir -p $(DESTDIR)$(PICSDIR)
	cp -rv $(PICS) $(DESTDIR)$(PICSDIR)

dependencies:
	$(eval files:=$(shell ./dependencies.sh))
	$(foreach file, $(files), `rpm2cpio $(file) | cpio -idmv -D $(DESTDIR)`)

package: install dependencies
	cd $(DESTDIR) && find . | cpio -c -o | gzip -9cv > $(OUTFILE)
	@echo "You can find the image at $(OUTFILE)"

uninstall:
	rm -rfv $(DESTDIR)$(ADDONDIR)
	#rm -rfv $(DESTDIR)$(PICSDIR)$(ICON)
	
