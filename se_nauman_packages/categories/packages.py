from pyanaconda.ui.categories import SpokeCategory

N_ = lambda x: x

__all__ = ["PackagesCategory"]


class PackagesCategory(SpokeCategory):
    displayOnHubGUI = "SummaryHub"
    displayOnHubTUI = "SummaryHub"
    title = N_("Additional Packages")
