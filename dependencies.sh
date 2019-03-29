#!/bin/bash
#sudo /usr/bin/dnf --downloaddir . --downloadonly reinstall python3-yubico python3-pyusb -y > /dev/null
/usr/bin/dnf download python3-yubico python3-pyusb > /dev/null
ls *.rpm

