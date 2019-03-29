from ...categories.packages import PackagesCategory
from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn
from pyanaconda.ui.gui.utils import escape_markup

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")

from gi.repository import Gtk, Pango

_ = lambda x: x
N_ = lambda x: x

__all__ = ["PackagesSpoke"]


class PackagesSpoke(FirstbootSpokeMixIn, NormalSpoke):
    builderObjects = ["packagesSpokeWindow"]
    mainWidgetName = "packagesSpokeWindow"
    uiFile = "packages.glade"
    category = PackagesCategory
    icon = "package-x-generic-symbolic"
    title = N_("_Packages")

    def __init__(self, data, storage, payload, instclass):
        NormalSpoke.__init__(self, data, storage, payload, instclass)

    def initialize(self):
        NormalSpoke.initialize(self)
        self._softwareListBox = self.builder.get_object("softwareListBox")
        self._countSelectedSoftware = 0

        for key, value in self.data.addons.se_nauman_packages.software.items():
            self._add_row(self._softwareListBox, key, value["Desc"], value["Active"])

            if value["Active"] is True:
                self._countSelectedSoftware += 1

    def refresh(self):
        self._handleList("refresh")

    def apply(self):
        self._handleList("apply")

    def execute(self):
        pass

    @property
    def ready(self):
        return True

    @property
    def completed(self):
        return True

    @property
    def mandatory(self):
        return False

    @property
    def status(self):
        return _("Selected software: {}".format(self._countSelectedSoftware))

    def _add_row(self, listbox, name, desc, selected=False):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        check = Gtk.CheckButton()
        check.set_active(selected)
        box.add(check)

        label = Gtk.Label(label="<b>%s</b>\n%s" % (escape_markup(name), escape_markup(desc)),
                          use_markup=True, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR,
                          hexpand=True, xalign=0, yalign=0.5)
        label.id = name
        box.add(label)

        row.add(box)
        listbox.insert(row, -1)

    def _handleList(self, direction):
        self._countSelectedSoftware = 0
        for (i, row) in enumerate(self._softwareListBox.get_children()):
            box = row.get_children()[0]
            button = box.get_children()[0]
            label = box.get_children()[1]
            if direction == "apply":
                software = self.data.addons.se_nauman_packages.software[label.id]
                software["Active"] = button.get_active()
                if software["Active"] is True and label.id not in self.data.packages.packageList:
                    self.data.packages.packageList.append(label.id)
                if software["Active"] is False and label.id in self.data.packages.packageList:
                    self.data.packages.packageList.remove(label.id)
            elif direction == "refresh":
                button.set_active(self.data.addons.se_nauman_packages.software[label.id]["Active"])

            if self.data.addons.se_nauman_packages.software[label.id]["Active"] is True:
                self._countSelectedSoftware += 1
