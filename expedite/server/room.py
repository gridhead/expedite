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


from expedite.config import standard
from expedite.server.conn import (
    exchange_insert,
    exchange_remove,
    exchange_inform,
    exchange_launch,
    exchange_gobyte,
    exchange_detail,
    exchange_digest,
    exchange_assert
)
from json import loads
from expedite.view import warning, general

from websockets.exceptions import ConnectionClosed


async def oper(sock):
    try:
        async for mesgcont in sock:
            if isinstance(mesgcont, str):
                mesgdict = loads(mesgcont)
                if mesgdict["call"] == "join":
                    identity = await exchange_insert(sock, mesgdict["plan"], mesgdict["scan"], mesgdict["wait"])
                    if identity:
                        pairpage = await exchange_inform(sock, mesgdict["plan"], mesgdict["scan"], identity)
                        if pairpage == 1:
                            otherend = standard.connection_dict[identity]["sock"]
                            await exchange_remove(otherend)
                            await exchange_remove(sock)
                            await otherend.close()
                            await sock.close()
                        elif pairpage == 2:
                            await exchange_remove(sock)
                            await sock.close()
                    else:
                        await sock.close()
                elif mesgdict["call"] == "meta":
                    await exchange_launch(sock, mesgdict["name"], mesgdict["size"])
                elif mesgdict["call"] == "drop":
                    await exchange_gobyte(sock)
                elif mesgdict["call"] == "hash":
                    await exchange_digest(sock, mesgdict["data"])
                elif mesgdict["call"] == "conf":
                    await exchange_assert(sock, mesgdict["data"])
                elif mesgdict["call"] == "rest":
                    await exchange_remove(sock)
            else:
                complete = await exchange_detail(sock, mesgcont)
                if not complete:
                    await exchange_remove(sock)
    except ConnectionClosed as expt:
        warning(f"Delivering client disconnected due to the disconnection of collecting client.")
        general(expt)
    finally:
        await exchange_remove(sock)
