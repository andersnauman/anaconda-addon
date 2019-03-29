#!/usr/bin/python3

import os

from initial_setup import InitialSetup, InitialSetupError

is_instance = InitialSetup(gui_mode=True)

try:
    is_instance.run()
except InitialSetupError:
    exit(1)

#if is_instance.reboot_on_quit:
#    os.system("reboot")

exit(0)