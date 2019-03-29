from pyanaconda.addons import AddonData
from pykickstart.options import KSOptionParser

__all__ = ["CryptoData"]


class CryptoData(AddonData):
    def __init__(self, name):
        AddonData.__init__(self, name)
        self.yubikey = False
        # self.enabled = False
        self.passphrase = ""

    def __str__(self):
        addon_str = "%addon {}".format(self.name)

        if self.yubikey:
            addon_str += " --{}".format(self.yubikey)

        # Do not add passphrase!

        # min-char
        # max-char

        addon_str += "\n%end\n"

        return addon_str

    def handle_header(self, lineno, args):
        op = KSOptionParser()
        op.add_option("--yubikey", action="store_true", default=False, dest="yubikey", help="")
        op.add_option("--passphrase", action="store_true", default="", dest="passphrase", help="")
        (opts, extra) = op.parse_args(args=args, lineno=lineno)
        self.yubikey = opts.yubikey
        self.passphrase = opts.passphrase

    def handle_line(self, line):
        pass

    def finalize(self):
        pass

    def setup(self, storage, ksdata, instclass, payload):
        pass

    def execute(self, storage, ksdata, instclass, users, payload):
        pass
