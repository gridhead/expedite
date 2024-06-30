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


from asyncio import get_event_loop, ensure_future
from websockets import connect
from websockets.exceptions import ConnectionClosed
from tqdm.asyncio import tqdm

import sys
from expedite.config import standard
from expedite.client.conn import (
    deliver_connection_to_server, 
    collect_permission_to_join, 
    deliver_suspension_from_expiry, 
    collect_connection_from_pairness,
    deliver_dropping_summon,
    collect_dropping_summon,
    collect_metadata,
    deliver_metadata,
    collect_contents,
    deliver_contents,
    deliver_digest_checks,
    collect_digest_checks,
    deliver_confirmation,
    collect_confirmation,
    facade_exit
)
from json import loads


async def oper():
    try:
        async with connect(standard.client_addr) as sock:
            get_event_loop().call_later(standard.client_time, lambda: ensure_future(deliver_suspension_from_expiry(sock)))
            await deliver_connection_to_server(sock)
            async for mesgcont in sock:
                if isinstance(mesgcont, str):
                    mesgdict = loads(mesgcont)
                    if mesgdict["call"] == "okay":
                        await collect_permission_to_join(mesgdict["iden"])
                    elif mesgdict["call"] == "meta":
                        await collect_metadata(mesgdict["name"], mesgdict["size"], mesgdict["chks"])
                        if standard.client_plan == "RECV":
                            await deliver_dropping_summon(sock)
                    elif mesgdict["call"] == "note":
                        await collect_connection_from_pairness(mesgdict["part"])
                        if standard.client_plan == "SEND":
                            await deliver_metadata(sock)
                    elif mesgdict["call"] == "drop":
                        await collect_dropping_summon()
                        if standard.client_plan == "SEND":
                            await deliver_contents(sock)
                            await deliver_digest_checks(sock)
                    elif mesgdict["call"] == "byte":
                        if standard.client_plan == "RECV":
                            await collect_contents(mesgdict["pack"])
                    elif mesgdict["call"] == "hash":
                        if standard.client_plan == "RECV":
                            await collect_digest_checks()
                            complete = await deliver_confirmation(sock, mesgdict["data"])
                            await facade_exit(sock, complete, "done" if complete else "dprt")
                    elif mesgdict["call"] == "conf":
                        if standard.client_plan == "SEND":
                            complete = await collect_confirmation(mesgdict["data"])
                            await facade_exit(sock, complete, "done" if complete else "dprt")
                    elif mesgdict["call"] in ["awry", "lone"]:
                        await facade_exit(sock, False, mesgdict["call"])
                else:
                    if standard.client_plan == "RECV":
                        await collect_contents(sock, mesgcont)
        sys.exit(standard.client_exit)
    except ConnectionClosed as expt:
        await facade_exit(sock, False, "dprt")
        sys.exit(standard.client_exit)
