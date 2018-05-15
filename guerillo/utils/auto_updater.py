import sys

import esky as esky


class AutoUpdater:

    @staticmethod
    def run():
        if hasattr(sys, "frozen"):
            app = esky.Esky(sys.executable, "http://guerillo.com/binaries/")
            app.auto_update()
