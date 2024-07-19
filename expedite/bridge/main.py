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


import sys
from asyncio import ensure_future, new_event_loop, set_event_loop
from os.path import basename

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from expedite.bridge.clct import CollectingOperations
from expedite.bridge.conn import Connection
from expedite.bridge.dlvr import DeliveringOperations
from expedite.bridge.util import ValidateFields
from expedite.bridge.wind import Ui_mainwind
from expedite.client.base import bite_file, find_size
from expedite.config import standard


class MainWindow(QMainWindow, CollectingOperations, DeliveringOperations, Connection):
    def __init__(self):
        super().__init__()
        self.loop = new_event_loop()
        set_event_loop(self.loop)
        self.ui = Ui_mainwind()
        self.ui.setupUi(self)
        self.normal_both_side()
        self.ui.dlvr_butn_browse.clicked.connect(self.handle_delivering_location)
        self.ui.clct_butn_browse.clicked.connect(self.handle_collecting_location)
        self.ui.dlvr_butn_random.clicked.connect(self.random_delivering_password)
        self.ui.clct_butn_random.clicked.connect(self.random_collecting_password)
        self.ui.dlvr_butn_normal.clicked.connect(self.normal_delivering_side)
        self.ui.clct_butn_normal.clicked.connect(self.normal_collecting_side)
        self.ui.dlvr_butn_incept.clicked.connect(self.incept_delivering_client)
        self.ui.clct_butn_incept.clicked.connect(self.incept_collecting_client)
        self.ui.progbarg.setMinimum(0)
        self.ui.progbarg.setMaximum(100)
        self.timekeeper = QTimer()
        self.timekeeper.timeout.connect(self.manage_events)
        self.timekeeper.start(1)

    def incept_delivering_client(self):
        if not standard.client_progress:
            report = ValidateFields().report_dlvr(
                self.ui.dlvr_line_size.text(),
                self.ui.dlvr_line_time.text(),
                self.ui.dlvr_line_file.text(),
                self.ui.dlvr_line_pswd.text()
            )
            if report[0] == (True, True, True, True):
                standard.client_plan = "SEND"
                standard.chunking_size = int(self.ui.dlvr_line_size.text())
                standard.client_time = int(self.ui.dlvr_line_time.text())
                standard.client_file = self.ui.dlvr_line_file.text()
                standard.client_pswd = self.ui.dlvr_line_pswd.text()
                standard.client_endo = self.ui.dlvr_line_endo.text()
                standard.client_filename = basename(standard.client_file)
                standard.client_filesize = find_size()
                standard.client_bind = bite_file()
                self.initialize_connection()
            else:
                self.show_dialog(QMessageBox.Warning, "Invalid information", f"Please correct the filled data\n\n{report[1]}")
        else:
            self.show_dialog(QMessageBox.Warning, "Ongoing interaction", "Please wait for the ongoing interaction to complete first before starting another or considering cancelling the interaction.")

    def incept_collecting_client(self):
        if not standard.client_progress:
            report = ValidateFields().report_clct(
                self.ui.clct_line_time.text(),
                self.ui.clct_line_file.text(),
                self.ui.clct_line_pswd.text()
            )
            if report[0] == (True, True, True):
                standard.client_plan = "RECV"
                standard.client_time = int(self.ui.clct_line_time.text())
                standard.client_file = self.ui.clct_line_file.text()
                standard.client_pswd = self.ui.clct_line_pswd.text()
                standard.client_endo = self.ui.clct_line_endo.text()
                standard.client_fileinit = False
                standard.client_metadone = False
                self.initialize_connection()
            else:
                self.show_dialog(QMessageBox.Warning, "Invalid information", f"Please correct the filled data\n\n{report[1]}")
        else:
            self.show_dialog(QMessageBox.Warning, "Ongoing interaction", "Please wait for the ongoing interaction to complete first before starting another or considering cancelling the interaction.")

    def initialize_connection(self):
        standard.client_host = self.ui.sockaddr.text()
        standard.client_progress = True
        self.ui.head_rqst.setText("Please wait while the client connects to the broker")
        ensure_future(self.maintain_connection())

    def normal_both_side(self):
        self.normal_delivering_side()
        self.normal_collecting_side()
        self.ui.head_rqst.setText("Please initialize the connection to acquire an identity")
        self.ui.head_iden.setText("INACCESSIBLE")
        self.ui.progbarg.setValue(0)
        self.ui.statarea.showMessage("READY")

    def manage_events(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def show_dialog(self, icon, head, data):
        dialog = QMessageBox(parent=self)
        dialog.setIcon(icon)
        dialog.setWindowTitle(f"Expedite - {head}")
        dialog.setText(data)
        dialog.exec()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
