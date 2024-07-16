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


class ValidateFields():
    def __init__(self):
        self.okay_size = False
        self.okay_time = False
        self.okay_file = False
        self.okay_pswd = False
        self.okay_path = False

    def verify_size(self, size):
        self.okay_size = True
        try:
            oper = int(size.strip())
            if oper not in range(1024, 524288):
                self.okay_size = False
        except ValueError:
            self.okay_size = False

    def verify_time(self, time):
        self.okay_time = True
        try:
            oper = int(time.strip())
            if oper not in range(5, 300):
                self.okay_time = False
        except ValueError:
            self.okay_time = False

    def verify_file(self, file):
        self.okay_file = True
        if not exists(file):
            self.okay_file = False

    def verify_path(self, path):
        self.okay_path = True
        if path.strip() != "" and not exists(path):
            self.okay_path = False

    def verify_pswd(self, pswd):
        self.okay_pswd = True
        if pswd.strip() == "":
            self.okay_pswd = False

    def report_dlvr(self, size, time, file, pswd):
        self.verify_size(size)
        self.verify_time(time)
        self.verify_file(file)
        self.verify_pswd(pswd)
        text_size = "" if self.okay_size else "Processing size must be an integer value between 1024 and 524288"
        text_time = "" if self.okay_time else "Expiry window must be an integer value between 5 and 300"
        text_file = "" if self.okay_file else "Filepath for delivering or collecting contents must exist"
        text_pswd = "" if self.okay_pswd else "Password cannot be an empty string"
        return (
            (self.okay_size, self.okay_time, self.okay_file, self.okay_pswd),
            "\n".join([text_size, text_time, text_file, text_pswd]).strip()
        )

    def report_clct(self, time, path, pswd):
        self.verify_time(time)
        self.verify_path(path)
        self.verify_pswd(pswd)
        text_time = "" if self.okay_time else "Expiry window must be an integer value between 5 and 300"
        text_path = "" if self.okay_path else "Filepath for delivering or collecting contents must exist"
        text_pswd = "" if self.okay_pswd else "Password cannot be an empty string"
        return (
            (self.okay_time, self.okay_path, self.okay_pswd),
            "\n".join([text_time, text_path, text_pswd]).strip(),
        )
