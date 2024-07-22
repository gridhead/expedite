"""
expedite
Copyright (C) 2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the codebase or documentation
are not subject to the GNU General Public License and may only be utilized or
replicated with the express permission of Red Hat, Inc.
"""


import os
import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from expedite.client.bridge import data  # noqa
from expedite.client.bridge.room import MainWindow


def load_custom_font():
    fontlist = [
        ":rsrc/axis/sans-bold.ttf",
        ":rsrc/axis/sans-rlar.ttf",
        ":rsrc/axis/sans-bdit.ttf",
        ":rsrc/axis/sans-rlit.ttf",
    ]
    for indx in fontlist:
        QFontDatabase.addApplicationFont(indx)


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)
    load_custom_font()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
