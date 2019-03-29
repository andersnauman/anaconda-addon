from pyanaconda.addons import AddonData

__all__ = ["AdditionalPackagesData"]


class AdditionalPackagesData(AddonData):
    def __init__(self, name):
        AddonData.__init__(self, name)
        self.software = {
            "wireshark": {
                "Desc": "Network traffic analyzer",
                "Active": False,
            },
            "nmap": {
                "Desc": "Network exploration tool and security scanner",
                "Active": False,
            },
            "gimp": {
                "Desc": "GNU Image Manipulation Program",
                "Active": False,
            },
            "Linux ISO": {
                "Desc": "linus och hans iso",
                "Active": False,
            },
        }

    def __str__(self):
        addon_str = "%addon {}".format(self.name)

        for key, value in self.software.items():
            if value["Active"] is True:
                addon_str += "\n{}".format(key)

        addon_str += "\n%end\n"

        return addon_str

    def handle_header(self, lineno, args):
        pass

    def handle_line(self, line):
        if line.strip() in self.software:
            self.software[line.strip()]["Active"] = True

    def finalize(self):
        pass

    def setup(self, storage, ksdata, instclass, payload):
        pass

    def execute(self, storage, ksdata, instclass, users, payload):
        pass
