from pyanaconda.ui.categories import SpokeCategory

N_ = lambda x: x

__all__ = ["CryptoCategory"]


class CryptoCategory(SpokeCategory):
    displayOnHubGUI = "SummaryHub"
    displayOnHubTUI = "SummaryHub"
    title = N_("Crypto")
