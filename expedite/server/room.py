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
from expedite.server.conn import exchange_insert, exchange_remove, exchange_inform, exchange_launch
from json import loads


async def oper(sockobjc):
    try:
        async for mesgtext in sockobjc:
            mesgdict = loads(mesgtext)
            if mesgdict["call"] == "join":
                identity = await exchange_insert(sockobjc, mesgdict["plan"], mesgdict["scan"], mesgdict["wait"])
                if identity:
                    pairpage = await exchange_inform(sockobjc, mesgdict["plan"], mesgdict["scan"], identity)
                    if pairpage == 1:
                        otherend = standard.connection_dict[identity]["sock"]
                        await exchange_remove(otherend)
                        await exchange_remove(sockobjc)
                        await otherend.close()
                        await sockobjc.close()
                    elif pairpage == 2:
                        await exchange_remove(sockobjc)
                        await sockobjc.close()
                else:
                    await sockobjc.close()
            elif mesgdict["call"] == "meta":
                await exchange_launch(mesgdict["part"], mesgdict["name"], mesgdict["size"])
            elif mesgdict["call"] == "rest":
                await exchange_remove(sockobjc)
                await sockobjc.close()
    finally:
        await exchange_remove(sockobjc)
