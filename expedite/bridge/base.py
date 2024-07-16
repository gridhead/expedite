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


from PySide6.QtWidgets import QFileDialog


def show_location_dialog(parent=None, oper: str = "") -> str:
    dialog = QFileDialog()
    if oper == "dlvr":
        client_path = dialog.getOpenFileName(parent, "Select location", "", "All Files (*)")[0]
    else:
        client_path = dialog.getExistingDirectory(parent, "Select location", "", QFileDialog.ShowDirsOnly)
    return client_path


def truncate_text(text: str = "", size: int = 32) -> str:
    if len(text) >= 32:
        return text[0:size-3] + "..."
    else:
        return text
