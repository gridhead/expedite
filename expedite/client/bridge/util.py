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


from os.path import exists

from PySide6.QtWidgets import QFileDialog


def show_location_dialog(parent=None, oper: str = "") -> str:
    """
    Select filepath for the intended file for delivering or collecting

    :param parent: Parent window within which the location dialog exists
    :param oper: Operation intent for choosing either file or directory
    :return:
    """
    dialog = QFileDialog()
    if oper == "dlvr":
        client_path = dialog.getOpenFileName(parent, "Select location", "", "All Files (*)")[0]
    else:
        client_path = dialog.getExistingDirectory(parent, "Select location", "", QFileDialog.ShowDirsOnly)
    return client_path


def truncate_text(text: str = "", size: int = 32) -> str:
    """
    Limit text elements to a certain character count for an elegant fit

    :param text: Text elements that need to be checked for fitting
    :param size: Character count within which text needs to be fit
    :return: Truncated text
    """
    if len(text) >= size:
        return text[0:size-3] + "..."
    else:
        return text


def return_detail_text() -> str:
    """
    Retrieve application information text for showing on the dialog box

    :return: Application information
    """
    text = """
    <b>Expedite Bridge v{vers}</b><br/>
    <i>A simple encrypted file transfer service for humans</i><br/><br/>
    Expedite is a simple encrypted file transfer service that allows for people to share synchronously assets among each other without having to rely on third party file sharing services (and constantly worrying about how their data might be used) or feeling the need of having publicly visible IP addresses (and constantly worrying about script kiddies attacking your computer).<br/><br/>
    Expedite Server can be deployed on a virtual private server having an IP address that is discoverable by the Expedite Client users to broker file contents. The transfers facilitated using WebSockets are end-to-end encrypted with the use of 128-bit Advanced Encryption Standard and the server is restricted to logging only unidentifiable activities to the volatile memory.<br/><br/>
    Expedite is currently in BETA phase and if you like to direction the project is heading towards, kindly consider helping me out by <a href="{star}">starring</a> the project repository, <a href="{tick}">filing</a> issue tickets for software errors or feature requests, <a href="{pull}">contributing</a> to the codebase of the project or <a href="{help}">sponsoring</a> me to help maintain the servers and to help me keep working on more FOSS projects like these.<br/><br/>
    """
    return text


class ValidateFields:
    def __init__(self) -> None:
        """
        Initialize fields validation class for confirmation

        :return:
        """
        self.okay = {
            "size": False,
            "time": False,
            "file": False,
            "path": False,
            "pswd": False,
        }
        self.text = {
            "size": "Processing size must be an integer value between 1024 and 524288",
            "time": "Expiry window must be an integer value between 5 and 300",
            "file": "Filepath for delivering or collecting contents must exist",
            "path": "Filepath for delivering or collecting contents must exist",
            "pswd": "Password cannot be an empty string"
        }

    def verify_size(self, size) -> None:
        """
        Ensure that processing size must be an integer value between 1024 and 524288

        :param size: Processing size
        :return:
        """
        self.okay["size"] = True
        try:
            oper = int(size.strip())
            if oper not in range(1024, 524288 + 1):
                self.okay["size"] = False
        except ValueError:
            self.okay["size"] = False

    def verify_time(self, time) -> None:
        """
        Ensure that expiry window must be an integer value between 5 and 300

        :param time: Expiry window
        :return:
        """
        self.okay["time"] = True
        try:
            oper = int(time.strip())
            if oper not in range(5, 300 + 1):
                self.okay["time"] = False
        except ValueError:
            self.okay["time"] = False

    def verify_file(self, file) -> None:
        """
        Ensure that filepath for delivering or collecting contents must exist

        :param file: Load filepath
        :return:
        """
        self.okay["file"] = True
        if not exists(file):
            self.okay["file"] = False

    def verify_path(self, path) -> None:
        """
        Ensure that filepath for delivering or collecting contents must exist

        :param path: Save filepath
        :return:
        """
        self.okay["path"] = True
        if path.strip() != "" and not exists(path):
            self.okay["path"] = False

    def verify_pswd(self, pswd) -> None:
        """
        Ensure that password cannot be an empty string

        :param pswd: Password string
        :return:
        """
        self.okay["pswd"] = True
        if pswd.strip() == "":
            self.okay["pswd"] = False

    def report_dlvr(self, size, time, file, pswd) -> tuple[tuple[bool, bool, bool, bool], str]:
        """
        Retrieve field validation results for delivering intent

        :param size: Validity confirmation of processing size
        :param time: Validity confirmation of waiting window
        :param file: Validity confirmation of delivering filepath
        :param pswd: Validity confirmation of password string
        :return: Validity confirmation for required elements
        """
        self.verify_size(size)
        self.verify_time(time)
        self.verify_file(file)
        self.verify_pswd(pswd)
        lict = [self.text[indx] for indx in ["size", "time", "file", "pswd"] if not self.okay[indx]]
        return (self.okay["size"], self.okay["time"], self.okay["file"], self.okay["pswd"]), "\n".join(lict).strip()

    def report_clct(self, time, path, pswd) -> tuple[tuple[bool, bool, bool], str]:
        """
        Retrieve field validation results for collecting intent

        :param time: Validity confirmation of waiting window
        :param path: Validity confirmation of collecting filepath
        :param pswd: Validity confirmation of password string
        :return: Validity confirmation for required elements
        """
        self.verify_time(time)
        self.verify_path(path)
        self.verify_pswd(pswd)
        lict = [self.text[indx] for indx in ["time", "path", "pswd"] if not self.okay[indx]]
        return (self.okay["time"], self.okay["path"], self.okay["pswd"]), "\n".join(lict).strip()
