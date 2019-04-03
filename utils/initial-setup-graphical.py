#!/usr/bin/python

import os

from initial_setup import InitialSetup, InitialSetupError

is_instance = InitialSetup(gui_mode=True)

try:
    is_instance.run()
except InitialSetupError:
    exit(1)
    
exit(0)