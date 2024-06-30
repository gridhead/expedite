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
are not subject to the GNU Affero General Public License and may only be used
or replicated with the express permission of Red Hat, Inc.
"""


import time

from expedite.view import warning, general, success, failure
from expedite.config import standard
from websockets.legacy.client import WebSocketClientProtocol


async def facade_exit(sock: WebSocketClientProtocol = None, cond: bool = True, note: str = "") -> None:
    if note != "done":
        warning(standard.notice_dict[note])
    if sock:
        await sock.close()
    plan = "Delivering" if standard.client_plan == "SEND" else "Collecting"
    if cond:
        success(f"{plan} done after {(time.time() - standard.client_strt):.2f} seconds.")
        standard.client_exit = 0
    else:
        failure(f"{plan} fail after {(time.time() - standard.client_strt):.2f} seconds.")
        standard.client_exit = 1
    general("Exiting.")
