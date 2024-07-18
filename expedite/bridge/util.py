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


class ValidateFields:
    def __init__(self):
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

    def verify_size(self, size):
        self.okay["size"] = True
        try:
            oper = int(size.strip())
            if oper not in range(1024, 524288 + 1):
                self.okay["size"] = False
        except ValueError:
            self.okay["size"] = False

    def verify_time(self, time):
        self.okay["time"] = True
        try:
            oper = int(time.strip())
            if oper not in range(5, 300 + 1):
                self.okay["time"] = False
        except ValueError:
            self.okay["time"] = False

    def verify_file(self, file):
        self.okay["file"] = True
        if not exists(file):
            self.okay["file"] = False

    def verify_path(self, path):
        self.okay["path"] = True
        if path.strip() != "" and not exists(path):
            self.okay["path"] = False

    def verify_pswd(self, pswd):
        self.okay["pswd"] = True
        if pswd.strip() == "":
            self.okay["pswd"] = False

    def report_dlvr(self, size, time, file, pswd):
        self.verify_size(size)
        self.verify_time(time)
        self.verify_file(file)
        self.verify_pswd(pswd)
        lict = [self.text[indx] for indx in ["size", "time", "file", "pswd"] if not self.okay[indx]]
        return (
            (self.okay["size"], self.okay["time"], self.okay["file"], self.okay["pswd"]),
            "\n".join(lict).strip()
        )

    def report_clct(self, time, path, pswd):
        self.verify_time(time)
        self.verify_path(path)
        self.verify_pswd(pswd)
        lict = [self.text[indx] for indx in ["time", "path", "pswd"] if not self.okay[indx]]
        return (
            (self.okay["time"], self.okay["path"], self.okay["pswd"]),
            "\n".join(lict).strip(),
        )
