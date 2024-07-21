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


def return_detail_text() -> str:
    text = """
    <b>Expedite v{vers}</b><br/>
    <i>A simple encrypted file transfer service for humans</i><br/><br/>
    Expedite is a simple encrypted file transfer service that allows for people to share synchronously assets among each other without having to rely on third party file sharing services (and constantly worrying about how their data might be used) or feeling the need of having publicly visible IP addresses (and constantly worrying about script kiddies attacking your computer).<br/><br/>
    Expedite Server can be deployed on a virtual private server having an IP address that is discoverable by the Expedite Client users to broker file contents. The transfers facilitated using WebSockets are end-to-end encrypted with the use of 128-bit Advanced Encryption Standard and the server is restricted to logging only unidentifiable activities to the volatile memory.<br/><br/>
    Expedite is currently in BETA phase and if you like to direction the project is heading towards, kindly consider helping me out by <a href="{star}">starring</a> the project repository, <a href="{tick}">filing</a> issue tickets for software errors or feature requests, <a href="{pull}">contributing</a> to the codebase of the project or <a href="{help}">sponsoring</a> me to help maintain the servers and to help me keep working on more FOSS projects like these.<br/><br/>
    """
    return text
