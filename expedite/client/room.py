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


import asyncio
from websockets import connect
from websockets.exceptions import ConnectionClosed

import sys
from expedite.config import standard
from expedite.view import failure, warning
from expedite.client.conn import (
    deliver_connection_to_server, 
    collect_permission_to_join, 
    deliver_suspension_from_expiry, 
    collect_connection_from_pairness, 
    collect_suspension_from_mismatch,
    collect_suspension_from_pairless,
    collect_metadata,
    deliver_metadata
)
from json import loads


async def oper():
    try:
        async with connect(standard.client_addr) as sockobjc:
            asyncio.get_event_loop().call_later(standard.client_time, lambda: asyncio.ensure_future(deliver_suspension_from_expiry(sockobjc)))
            await deliver_connection_to_server(sockobjc)
            async for mesgtext in sockobjc:
                mesgdict = loads(mesgtext)
                if mesgdict["call"] == "okay":
                    await collect_permission_to_join(mesgdict["iden"])
                elif mesgdict["call"] == "note":
                    await collect_connection_from_pairness(mesgdict["iden"])
                    if standard.client_plan == "SEND":
                        await deliver_metadata(sockobjc)
                elif mesgdict["call"] == "awry":
                    await collect_suspension_from_mismatch(mesgdict["iden"])
                    await sockobjc.close()
                    sys.exit(1)
                elif mesgdict["call"] == "lone":
                    await collect_suspension_from_pairless(mesgdict["iden"])
                    await sockobjc.close()
                    sys.exit(1)
                elif mesgdict["call"] == "meta":
                    await collect_metadata(mesgdict["name"], mesgdict["size"])
    except ConnectionClosed as expt:
        warning(f"{expt}")
        failure("Exiting.")
        sys.exit(1)
