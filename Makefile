ADDON = se_nauman_packages se_nauman_crypto
ADDONDIR = /usr/share/anaconda/addons/
PICS = pics/
PICSDIR = /usr/share/anaconda/pixmaps/
OUTFILE = /tmp/anaconda_addon.img

all:
	@echo "usage:"
	@echo "   make install"
	@echo "   make uninstall"
	@echo "   make package"
	@echo "   make package DESTDIR=`mktemp -d`"

install:
	mkdir -p $(DESTDIR)$(ADDONDIR)
	
	# Dependencies
	$(eval files:=$(shell ./dependencies.sh))
	$(foreach file, $(files), `rpm2cpio $(file) | cpio -idmvD $(DESTDIR)`)
	
	# Addon
	cp -rv $(ADDON) $(DESTDIR)$(ADDONDIR)
	
	# Logo / Background	
	mkdir -p $(DESTDIR)$(PICSDIR)
	cp -rv $(PICS) $(DESTDIR)$(PICSDIR)

package: install
	cd $(DESTDIR) && find . | cpio -c -o | gzip -9cv > $(OUTFILE)
	@echo "You can find the image at $(OUTFILE)"

uninstall:
	rm -rfv $(DESTDIR)$(ADDONDIR)
	#rm -rfv $(DESTDIR)$(PICSDIR)$(ICON)
	
