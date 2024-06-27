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


from json import dumps
from expedite.view import warning, general, failure
from expedite.config import standard


async def insert(sockobjc) -> bool:
    mesgdict = {
        "call": "join",
        "plan": standard.client_plan,
        "scan": standard.client_endo,
        "wait": standard.client_time
    }
    mesgtext = dumps(mesgdict)
    general("Attempting to connect to the network.")
    try:
        await sockobjc.send(mesgtext)
        return True
    except Exception as expt:
        warning(f"Failed to connect to the network - {expt}.")
        return False


async def identify_permission(iden: str = standard.client_iden) -> bool:
    standard.client_iden = iden
    general(f"Successfully connected to the network.")
    warning(f"You are now identified as {iden} in the network.")
    return True


async def expiry_exit(sockobjc) -> bool:
    if not standard.client_pair:
        mesgdict = {
            "call": "rest",
            "iden": standard.client_iden,
        }
        mesgtext = dumps(mesgdict)
        warning("Attempting to abandon from the network after expiry")
        try:
            await sockobjc.send(mesgtext)
            failure("Exiting")
            return True
        except Exception as expt:
            warning(f"Failed to abandon from the network - {expt}.")
            return False
    else:
        return False


async def jump_transmission(iden: str = standard.client_endo) -> bool:
    standard.client_endo = iden
    standard.client_pair = True
    general(f"Attempting pairing with {standard.client_endo}.")
    warning(f"Starting transmission.")
    return True


async def kill_transmission(iden: str = standard.client_endo) -> bool:
    standard.client_endo = iden
    general(f"Attempting pairing with {standard.client_endo}.")
    warning(f"Mismatch interactions.")
    failure(f"Exiting.")
    return True


async def lone_transmission(iden: str = standard.client_endo) -> bool:
    standard.client_endo = iden
    general(f"Attempting pairing with {standard.client_endo}.")
    warning(f"Hitherto paired.")
    failure(f"Exiting.")
    return True
