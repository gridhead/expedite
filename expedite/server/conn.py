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


from expedite.view import warning, success, failure, general
from expedite.config import standard
from uuid import uuid4
from json import dumps
from websockets.legacy.server import WebSocketServerProtocol


async def exchange_insert(sock: WebSocketServerProtocol, plan: str = standard.client_plan, scan: str = standard.client_endo, time: int = standard.client_time) -> str | bool:
    if sock not in standard.connection_dict:
        if plan in ["SEND", "RECV"]:
            identity = uuid4().hex[0:8].upper()
            standard.connection_dict[sock] = {
                "iden": identity,
                "plan": plan,
                "scan": scan if scan != "" else None,
                "time": time,
                "pair": False,
                "ptid": "",
                "ptsc": None
            }
            if plan == "SEND":
                warning(f"{identity} joined with the intention of delivering.")
            elif plan == "RECV":
                warning(f"{identity} joined with the intention of collecting.")
            if scan == "":
                general(f"{identity} is waiting for client for {time} seconds.")
            else:
                general(f"{identity} is looking for {scan} for {time} seconds.")
            await sock.send(dumps({"call": "okay", "iden": identity}))
            return identity
        else:
            return False
    else:
        return False


async def exchange_remove(sock: WebSocketServerProtocol) -> bool:
    if sock in standard.connection_dict:
        if standard.connection_dict[sock]["ptsc"] in standard.connection_dict and standard.connection_dict[sock]["ptsc"].state == 1:
            warning(f"{standard.connection_dict[sock]["ptid"]} left.")
            await standard.connection_dict[sock]["ptsc"].close(code=1000)
            standard.connection_dict.pop(standard.connection_dict[sock]["ptsc"])
        warning(f"{standard.connection_dict[sock]["iden"]} left.")
        await sock.close(code=1000)
        standard.connection_dict.pop(sock)
        return True
    else:
        return False


async def exchange_inform(sock: WebSocketServerProtocol, plan: str = standard.client_plan, scan: str = standard.client_endo, iden: str = standard.client_iden) -> int:
    for indx in standard.connection_dict:
        if standard.connection_dict[indx]["iden"] == scan:
            if not standard.connection_dict[indx]["pair"]:
                if plan != standard.connection_dict[indx]["plan"]:
                    success(f"{iden} and {scan} are positively paired.")
                    await indx.send(dumps({"call": "note", "part": iden}))
                    await sock.send(dumps({"call": "note", "part": scan}))
                    standard.connection_dict[indx]["pair"], standard.connection_dict[sock]["pair"] = True, True
                    standard.connection_dict[indx]["ptid"], standard.connection_dict[sock]["ptid"] = iden, scan
                    standard.connection_dict[indx]["ptid"], standard.connection_dict[sock]["ptid"] = iden, scan
                    standard.connection_dict[indx]["ptsc"], standard.connection_dict[sock]["ptsc"] = sock, indx
                    return 0
                else:
                    failure(f"{iden} and {scan} are negatively paired.")
                    await indx.send(dumps({"call": "awry", "part": iden}))
                    await sock.send(dumps({"call": "awry", "part": scan}))
                    return 1
            else:
                failure(f"{iden} and {scan} cannot pair as {scan} is already paired.")
                await sock.send(dumps({"call": "lone", "part": scan}))
                return 2
    return 3


async def exchange_json(sock: WebSocketServerProtocol, note: str = "", data: str = "") -> bool:
    general(standard.server_note[note].format(sj=standard.connection_dict[sock]["iden"], oj=standard.connection_dict[sock]["ptid"]))
    if sock in standard.connection_dict:
        if standard.connection_dict[sock]["ptsc"] in standard.connection_dict and standard.connection_dict[sock]["ptsc"].state == 1:
            await standard.connection_dict[sock]["ptsc"].send(data)
            return True
        else:
            return False
    else:
        return False


async def exchange_byte(sock: WebSocketServerProtocol, pack: bytes = b"") -> bool:
    if sock in standard.connection_dict:
        if standard.connection_dict[sock]["ptsc"] in standard.connection_dict and standard.connection_dict[sock]["ptsc"].state == 1:
            await standard.connection_dict[sock]["ptsc"].send(pack)
            return True
        else:
            general(f"{standard.connection_dict[sock]["iden"]} could not deliver contents to {standard.connection_dict[sock]["ptid"]} as {standard.connection_dict[sock]["ptid"]} is no longer connected.")
            return False
    else:
        general("Attempting for aborting connection.")
        return False
