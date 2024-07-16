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


from expedite.bridge.base import show_location_dialog
from expedite.client.base import ease_size
from expedite.config import standard
from expedite.bridge.base import truncate_text
from os.path import basename, getsize

from uuid import uuid4


class DeliveringOperations():
    def __init__(self):
        pass

    def handle_delivering_location(self):
        path = show_location_dialog(self, "dlvr")
        if path:
            self.ui.dlvr_line_file.setText(path)
            self.ui.dlvr_head_file.setText(f"Delivering <b>{truncate_text(basename(path), 28)}</b> ({ease_size(getsize(path))})")

    def normal_delivering_side(self):
        self.ui.dlvr_head_file.setText("No file selected")
        self.ui.dlvr_line_size.setText(str(standard.chunking_size))
        self.ui.dlvr_line_time.setText(str(standard.client_time))
        self.ui.dlvr_line_file.clear()
        self.ui.dlvr_line_pswd.clear()
        self.ui.dlvr_line_endo.clear()

    def random_delivering_password(self):
        self.ui.dlvr_line_pswd.setText(uuid4().hex[0:16].upper())
