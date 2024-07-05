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
    exchange_byte,
    exchange_json,
)
from json import loads
from expedite.view import warning, general, failure

from websockets.exceptions import ConnectionClosed


async def oper(sock):
    try:
        async for mesgcont in sock:
            if isinstance(mesgcont, str):
                mesgdict = loads(mesgcont)
                if mesgdict["call"] == "join":
                    identity = await exchange_insert(sock, mesgdict["plan"], mesgdict["scan"], mesgdict["wait"])
                    if bool(identity):
                        if await exchange_inform(sock, mesgdict["plan"], mesgdict["scan"], identity) in [1, 2]:
                            await exchange_remove(sock)
                    else:
                        await sock.close()
                elif mesgdict["call"] in ["meta", "drop", "hash", "conf", "flub"]:
                    await exchange_json(sock, mesgdict["call"], mesgcont)
                elif mesgdict["call"] == "rest":
                    failure(f"{standard.connection_dict[sock]["iden"]} has achieved expiry.")
                    await exchange_remove(sock)
            else:
                await exchange_byte(sock, mesgcont)
    except ConnectionClosed as expt:
        warning(f"Delivering client disconnected due to the disconnection of collecting client.")
        general(expt)
    finally:
        await exchange_remove(sock)
