from ...categories.crypto import CryptoCategory
from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn

from secrets import SystemRandom
import string
import yubico

from pyanaconda.modules.common.constants.objects import AUTO_PARTITIONING
from pyanaconda.modules.common.constants.services import STORAGE


_ = lambda x: x
N_ = lambda x: x

__all__ = ["CryptoSpoke"]


class CryptoSpoke(FirstbootSpokeMixIn, NormalSpoke):
    builderObjects = ["cryptoSpokeWindow"]
    mainWidgetName = "cryptoSpokeWindow"
    uiFile = "crypto.glade"
    category = CryptoCategory
    icon = "drive-harddisk-symbolic"
    title = N_("_Disk Crypto")

    def __init__(self, data, storage, payload, instclass):
        NormalSpoke.__init__(self, data, storage, payload, instclass)

        # Yubikey settings
        self._yubikeyActive = self.data.addons.se_nauman_crypto.yubikey
        self._yubikeyVersion = 0
        self._yubikeyCheckBox = None

        # Storage settings
        #   Storage-spoke need to be synced.
        self._auto_part_observer = STORAGE.get_observer(AUTO_PARTITIONING)
        self._auto_part_observer.connect()
        #   Passphrase to use
        #   Real phrase is set to self.storage.encryption_passphrase later
        self.passphrase = self.data.addons.se_nauman_crypto.passphrase
        #   Generate and set passphrase
        self._updateDiskCrypto()

    def initialize(self):
        NormalSpoke.initialize(self)
        self._yubikeyCheckBox = self.builder.get_object("yubikey")

    def refresh(self):
        self._yubikeyCheckBox.set_active(self._yubikeyActive)

    def apply(self):
        self._yubikeyActive = self._yubikeyCheckBox.get_active()

        if self.data.addons.se_nauman_crypto.yubikey is not self._yubikeyActive:
            self.data.addons.se_nauman_crypto.yubikey = self._yubikeyActive

        self._updateDiskCrypto()

    def execute(self):
        # Set passphrase on yubikey
        pass

    @property
    def ready(self):
        return True

    @property
    def completed(self):
        if self.storage.encryption_passphrase == "":
            return False

        if self._yubikeyActive is True:
            try:
                self._getYubikey()
            except ValueError:
                return False

        return True

    @property
    def mandatory(self):
        return True

    @property
    def status(self):
        status = "Using yubikey: {}".format(self._yubikeyActive)
        if self._yubikeyActive is True:
            try:
                self._getYubikey()
            except ValueError as e:
                status += "\nYubikey Status: {}".format(e)
            else:
                status += "\nYubikey Status: {}".format(self._yubikeyVersion)

        if self.passphrase != "":
            status += "\nCrypto key:\n{}".format(self.passphrase)
        else:
            status += "\nCrypto key: None\n"

        return _(status)

    def _updateDiskCrypto(self):
        # If passphrase is empty, create one.
        if self.passphrase == "":
            self.passphrase = "".join(SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20))

        self._auto_part_observer.proxy.SetPassphrase(self.passphrase)
        self.storage.encryption_passphrase = self._auto_part_observer.proxy.Passphrase
        if self.storage.encrypted_autopart is False:
            self.storage.encrypted_autopart = True

    def _getYubikey(self):
        try:
            skip = 0
            while skip < 5:
                yubikey = yubico.find_yubikey(skip=skip)
                skip += 1
        except yubico.yubikey.YubiKeyError:
            pass

        if skip == 0:
            raise ValueError("No yubikey were found")
        if skip > 1:
            raise ValueError("Too many yubikey:s were found")

        return yubikey
