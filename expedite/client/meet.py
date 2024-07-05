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


from expedite import __versdata__
from expedite.config import standard
from expedite.view import general, success, warning


def talk() -> None:
    success(f"Expedite Client v{__versdata__}")
    general(f"Addr. {standard.client_addr}")
    general(f"Pass. {standard.client_pswd}")
    if standard.client_plan == "SEND":
        general("Plan. DELIVERING")
    elif standard.client_plan == "RECV":
        general("Plan. COLLECTING")
    general(f"Wait. {standard.client_time} seconds")
    if standard.client_endo == "":
        warning("Please share your acquired identity to begin interaction.")
    else:
        warning(f"Please wait for {standard.client_endo} to begin interaction.")
