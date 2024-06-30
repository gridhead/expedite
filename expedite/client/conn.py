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
import time
from json import dumps
from expedite.view import warning, general
from expedite.config import standard
from websockets.legacy.client import WebSocketClientProtocol
from expedite.client.base import ease_size, read_file, fuse_file
from hashlib import sha256
from expedite.client.util import facade_exit
from tqdm.asyncio import trange
from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm.asyncio import tqdm
from datetime import datetime


async def deliver_connection_to_server(sock: WebSocketClientProtocol) -> bool:
    general("Attempting to connect to the network.")
    try:
        await sock.send(dumps({"call": "join", "plan": standard.client_plan, "scan": standard.client_endo, "wait": standard.client_time}))
        return True
    except Exception as expt:
        warning(f"Failed to connect to the network - {expt}.")
        return False


async def collect_permission_to_join(iden: str = standard.client_iden) -> bool:
    standard.client_iden = iden
    general(f"Successfully connected to the network.")
    warning(f"You are now identified as {iden} in the network.")
    return True


async def deliver_suspension_from_expiry(sock: WebSocketClientProtocol) -> None | bool:
    if not standard.client_pair:
        general("Attempting to abandon from the network after expiry.")
        await sock.send(dumps({"call": "rest"}))
        await facade_exit(sock, False, "rest")
    else:
        return False


async def collect_connection_from_pairness(iden: str = standard.client_endo) -> bool:
    standard.client_endo = iden
    standard.client_pair = True
    general(f"Attempting pairing with {standard.client_endo}.")
    warning(f"Starting transmission.")
    return True


async def collect_metadata(name: str = standard.client_filename, size: str = standard.client_filesize, chks: int = standard.client_chks) -> bool:
    standard.client_filename, standard.client_filesize, standard.client_chks = name, size, chks
    general(f"Collecting metadata for '{standard.client_filename}' ({ease_size(standard.client_filesize)}) from {standard.client_endo}.")
    return True


async def deliver_metadata(sock: WebSocketClientProtocol):
    await sock.send(dumps({"call": "meta", "name": standard.client_filename, "size": standard.client_filesize, "chks": len(standard.client_bind)-1}))
    general(f"Delivering metadata for '{standard.client_filename}' ({ease_size(standard.client_filesize)}) to {standard.client_endo}.")
    return True


async def deliver_dropping_summon(sock: WebSocketClientProtocol) -> bool:
    await sock.send(dumps({"call": "drop"}))
    general(f"Delivering collection summon to {standard.client_endo}.")
    return True


async def collect_dropping_summon() -> bool:
    general(f"Collecting delivering summon from {standard.client_endo}.")
    return True


async def deliver_contents(sock: WebSocketClientProtocol) -> bool:
    with logging_redirect_tqdm():
        with tqdm(total=standard.client_filesize, unit="B", unit_scale=True, unit_divisor=1024, leave=False, initial=0) as prog:
            for indx in range(0, len(standard.client_bind) - 1):
                bite = read_file(standard.client_bind[indx], standard.client_bind[indx + 1])
                prog.set_description(f"{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} SHA256 {sha256(bite).hexdigest()}")
                prog.update(standard.client_bind[indx + 1] - standard.client_bind[indx])
                await sock.send(bite)
                await asyncio.sleep(0)
        return True


async def collect_contents(sock: WebSocketClientProtocol, pack: bytes = b"") -> bool:
    fuse_file(pack)
    with logging_redirect_tqdm():
        with tqdm(total=standard.client_filesize, unit="B", unit_scale=True, unit_divisor=1024, leave=False, initial=len(pack)) as prog:
            for indx in range(standard.client_chks - 1):
                mesgcont = await sock.recv()
                if isinstance(mesgcont, bytes):
                    fuse_file(mesgcont)
                    prog.set_description(f"{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} SHA256 {sha256(mesgcont).hexdigest()}")
                    prog.update(len(mesgcont))
                    await asyncio.sleep(0)
    return True


async def deliver_digest_checks(sock: WebSocketClientProtocol) -> bool:
    general(f"Delivering contents digest for confirmation.")
    await sock.send(dumps({"call": "hash", "data": standard.client_hash.hexdigest()}))
    return True


async def collect_digest_checks() -> bool:
    general(f"Collecting contents digest for confirmation.")
    return True


async def deliver_confirmation(sock: WebSocketClientProtocol, data: str = standard.client_hash.hexdigest()) -> bool:
    if data == standard.client_hash.hexdigest():
        general(f"Contents integrity verified.")
        await sock.send(dumps({"call": "conf", "data": 1}))
        return True
    else:
        general(f"Contents integrity mismatch.")
        await sock.send(dumps({"call": "conf", "data": 0}))
        return False


async def collect_confirmation(data: int = 0) -> bool:
    if bool(data):
        general(f"Contents integrity verified.")
        return True
    else:
        general(f"Contents integrity mismatch.")
        return False
