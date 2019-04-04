# -*- coding: utf-8 -*-

from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn
from pyanaconda.ui.categories.system import SystemCategory

from secrets import SystemRandom
import string
import yubico
import binascii
import os
from Crypto.Cipher import AES

from pyanaconda.modules.common.constants.objects import AUTO_PARTITIONING
from pyanaconda.modules.common.constants.services import STORAGE


_ = lambda x: x
N_ = lambda x: x

__all__ = ["CryptoSpoke"]


class CryptoSpoke(FirstbootSpokeMixIn, NormalSpoke):
    builderObjects = ["cryptoSpokeWindow"]
    mainWidgetName = "cryptoSpokeWindow"
    uiFile = "crypto.glade"
    category = SystemCategory
    icon = "drive-harddisk-symbolic"
    title = N_("_DISK ENCRYPTION")

    def __init__(self, data, storage, payload, instclass):
        NormalSpoke.__init__(self, data, storage, payload, instclass)

        # Yubikey settings
        self._yubikey = None
        self._yubikeyActive = self.data.addons.se_nauman_crypto.yubikey
        self._yubikeyVersion = 0
        self._yubikeyCheckBox = None
        self._yubikeyError = ""

        # Storage settings
        #   Storage-spoke need to be synced.
        self._auto_part_observer = STORAGE.get_observer(AUTO_PARTITIONING)
        self._auto_part_observer.connect()
        #   Passphrase to use
        #   Real phrase is set to self.storage.encryption_passphrase later
        self._passphrase = self.data.addons.se_nauman_crypto.passphrase
        self._length = self.data.addons.se_nauman_crypto.length
        self._newPassphrase = False

    def initialize(self):
        NormalSpoke.initialize(self)
        self._yubikeyCheckBox = self.builder.get_object("yubikey")

        # Get Yubikey. Will assign self._yubikey and set self._yubikeyVersion
        try:
            self._getYubikey()
        except ValueError as e:
            self._yubikeyError = e
            return
        
        #   Generate and set passphrase
        self._updateDiskCrypto()

    def refresh(self):
        self._yubikeyCheckBox.set_active(self._yubikeyActive)

    def apply(self):
        self._yubikeyActive = self._yubikeyCheckBox.get_active()

        if self.data.addons.se_nauman_crypto.yubikey is not self._yubikeyActive:
            self.data.addons.se_nauman_crypto.yubikey = self._yubikeyActive
            self._newPassphrase = True 

        self._updateDiskCrypto()

    def execute(self):
        pass

    @property
    def ready(self):
        return True

    @property
    def completed(self):
        if self.storage.encryption_passphrase == "":
            return False

        if self._yubikeyActive is True and self._yubikeyVersion == 0:
            return False

        return True

    @property
    def mandatory(self):
        return True

    @property
    def status(self):
        status = "Using yubikey: {}".format(self._yubikeyActive)
        if self._yubikeyActive is True:
            if self._yubikeyVersion == 0 or self._yubikeyError != "":
                status += "\nStatus: {}".format(self._yubikeyError)
            else:
                status += "\nStatus: {}".format(self._yubikeyVersion)

        if self._passphrase != "":
            status += "\nKey: {}".format(self._passphrase)
        else:
            status += "\nKey: None\n"

        return _(status)

    def _updateDiskCrypto(self):
        # If passphrase is empty, create one.
        if self._passphrase == "" or self._newPassphrase is True:
            if self._yubikeyActive is True:
                try:
                    self._passphrase = self._generateKey()
                except ValueError as e:
                    self._yubikeyError = e
                    self._passphrase = ""
            else:
                self._passphrase = "".join(SystemRandom().choice(string.ascii_letters + string.digits + "!#%&/()=@£${}[]'*-_.,;:<>|".decode('utf8')) for _ in range(20))
            self._newPassphrase = False

        self._auto_part_observer.proxy.SetPassphrase(self._passphrase)
        self.storage.encryption_passphrase = self._auto_part_observer.proxy.Passphrase
        if self.storage.encrypted_autopart is False:
            self.storage.encrypted_autopart = True

    def _getYubikey(self):
        try:
            skip = 0
            while skip < 5:
                yk = yubico.find_yubikey(skip=skip)
                if yk is not None:
                    self._yubikey = yk # Assumes that only one yubikey could be found. 
                skip += 1
        except yubico.yubikey.YubiKeyError:
            pass

        if skip == 0:
            self._yubikey = None
            raise ValueError("No yubikey were found")
        if skip > 1:
            self._yubikey = None
            raise ValueError("Too many yubikey:s were found")

        self._yubikeyVersion = self._yubikey.version()

    def _generateKey(self):
        if self._yubikey is None:
            raise ValueError("No yubikey available")

        key = binascii.hexlify(os.urandom(16))
        keyFixed = binascii.hexlify(os.urandom(16))

        cfg = self._yubikey.init_config()
        cfg.aes_key("h:" + key.decode("utf-8"))
        cfg.config_flag('STATIC_TICKET', True)
        cfg.fixed_string("h:" + keyFixed.decode("utf-8"))

        try:
            self._yubikey.write_config(cfg, slot=1) 
        except:
            raise ValueError("Write error")

        return self._predict(key, keyFixed)
        
    def _predict(self, key, keyFixed):
        fixed = b'000000000000ffffffffffffffff0f2e' # Magic static key, undocumented?
        enc = AES.new(binascii.unhexlify(key), AES.MODE_CBC, b'\x00' * 16)
        data = enc.encrypt(binascii.unhexlify(fixed))
        
        # Translate to scan code safe string.
        try:
            # Python 2
            maketrans = string.maketrans
        except AttributeError:
            # Python 3
            maketrans = bytes.maketrans
        t_map = maketrans(b"0123456789abcdef", b"cbdefghijklnrtuv")

        outKey = binascii.hexlify(data).translate(t_map).decode("utf-8")
        outKeyFixed = keyFixed.decode("utf-8").translate(t_map)

        return outKeyFixed + outKey

