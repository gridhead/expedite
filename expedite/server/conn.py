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


from expedite.view import warning, success, failure
from expedite.config import standard
from uuid import uuid4
from json import dumps


async def exchange_insert(sockobjc, plan: str, scan: str, time: int) -> str | bool:
    if sockobjc not in standard.connection_list:
        if plan in ["SEND", "RECV"]:
            identity = uuid4().hex[0:8].upper()
            standard.connection_dict[identity] = {
                "sock": sockobjc,
                "plan": plan,
                "scan": scan if scan != "" else None,
                "time": time,
                "pair": False,
                "part": "",
            }
            standard.connection_list.add(sockobjc)
            if plan == "SEND":
                warning(f"{identity} joined with the intention of delivering.")
            elif plan == "RECV":
                warning(f"{identity} joined with the intention of collecting.")
            if scan == "":
                warning(f"{identity} is waiting for client for {time} seconds.")
            else:
                warning(f"{identity} is looking for {scan} for {time} seconds.")
            await sockobjc.send(dumps({"call": "okay", "iden": identity}))
            return identity
        else:
            return False
    else:
        return False


async def exchange_remove(sockobjc) -> bool:
    if sockobjc not in standard.connection_list:
        return False
    else:
        identity = ""
        for indx in standard.connection_dict:
            if standard.connection_dict[indx]["sock"] == sockobjc:
                identity = indx
        standard.connection_dict.pop(identity)
        standard.connection_list.remove(sockobjc)
        warning(f"{identity} left.")
        return True


async def exchange_inform(sockobjc, plan: str, scan: str, iden: str) -> int:
    if scan in standard.connection_dict:
        otherend = standard.connection_dict[scan]["sock"]
        if not standard.connection_dict[scan]["pair"]:
            if plan != standard.connection_dict[scan]["plan"]:
                success(f"{iden} and {scan} are positively paired.")
                await otherend.send(dumps({"call": "note", "iden": iden}))
                await sockobjc.send(dumps({"call": "note", "iden": scan}))
                standard.connection_dict[iden]["pair"] = True
                standard.connection_dict[iden]["part"] = scan
                standard.connection_dict[scan]["pair"] = True
                standard.connection_dict[scan]["part"] = iden
                return 0
            else:
                failure(f"{iden} and {scan} are negatively paired.")
                await otherend.send(dumps({"call": "awry", "iden": iden}))
                await sockobjc.send(dumps({"call": "awry", "iden": scan}))
                return 1
        else:
            failure(f"{iden} and {scan} cannot pair as {scan} is already paired.")
            await sockobjc.send(dumps({"call": "lone", "iden": scan}))
            return 2
    else:
        return 3


async def exchange_launch(iden: str = standard.client_iden, name: str = standard.client_filename, size: str = standard.client_filesize):
    warning(f"{standard.connection_dict[iden]["part"]} attempting to share file metadata to {iden}.")
    if iden in standard.connection_dict:
        otherend = standard.connection_dict[iden]["sock"]
        await otherend.send(dumps({"call": "meta", "part": standard.connection_dict[iden]["part"], "name": name, "size": size}))
        return True
    else:
        return False
