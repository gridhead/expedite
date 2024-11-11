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
are not subject to the GNU General Public License and may only be utilized or
replicated with the express permission of Red Hat, Inc.
"""


import asyncio
import time
from hashlib import sha256
from json import dumps
from typing import Generator, Tuple

from websockets.legacy.client import WebSocketClientProtocol

from expedite.client.auth import decr_metadata, encr_metadata
from expedite.client.base import ease_size, fuse_file, read_file
from expedite.client.excp import PasswordMistaken
from expedite.config import standard
from expedite.view import general, warning


async def deliver_connection_to_server(sock: WebSocketClientProtocol) -> bool:
    """
    Inform target client of connecting to the exchange server

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    general("Attempting to connect to the network.")
    try:
        await sock.send(dumps({"call": "join", "plan": standard.client_plan, "scan": standard.client_endo, "wait": standard.client_time}))
        return True
    except Exception as expt:
        warning(f"Failed to connect to the network - {expt}.")
        return False


async def collect_connection_to_server(iden: str = standard.client_iden) -> bool:
    """
    Show textual message of connecting to the exchange server

    :param iden: Network identity of person client
    :return: Confirmation of the action completion
    """
    standard.client_iden = iden
    general("Successfully connected to the network.")
    warning(f"You are now identified as {iden} in the network.")
    return True


async def deliver_suspension_from_expiry(sock: WebSocketClientProtocol) -> bool:
    """
    Inform exchange server about the disconnection from timed expiry

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    if not standard.client_pair:
        general("Attempting to abandon from the network after expiry.")
        await sock.send(dumps({"call": "rest"}))
        return True
    else:
        return False


async def collect_connection_from_pairness(iden: str = standard.client_endo) -> bool:
    """
    Show textual message of collecting confirmation of pairing

    :param iden: Network identity of target client
    :return: Confirmation of the action completion
    """
    standard.client_endo = iden
    standard.client_pair = True
    general(f"Attempting pairing with {standard.client_endo}.")
    warning("Starting transmission.")
    return True


async def deliver_metadata(sock: WebSocketClientProtocol) -> bool:
    """
    Inform target client of encrypting and delivering the metadata

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    general("Generating cryptography sign.")
    await sock.send(encr_metadata())
    return True


async def collect_metadata(pack: bytes = b"") -> bool:
    """
    Show textual message of collecting and decrypting the metadata

    :param pack: Encrypted metadata collected from target client
    :return: Confirmation of the action completion
    """
    try:
        general("Generating cryptography sign.")
        standard.client_filename, standard.client_filesize, standard.client_chks = decr_metadata(pack)
        return True
    except PasswordMistaken:
        return False


async def deliver_dropping_summon(sock: WebSocketClientProtocol) -> bool:
    """
    Inform target client of starting the exchange process

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    await sock.send(dumps({"call": "drop"}))
    general(f"Delivering collection summon to {standard.client_endo}.")
    return True


async def collect_dropping_summon() -> bool:
    """
    Show textual message of starting the exchange process

    :return: Confirmation of the action completion
    """
    general(f"Collecting delivering summon from {standard.client_endo}.")
    return True


async def deliver_contents(sock: WebSocketClientProtocol) -> Generator[Tuple[bytes, int], None, None]:
    """
    Load contents from intended file and deliver them to target client

    :param sock: Websocket object belonging to the server session
    :return: Tuple of file contents and contents length
    """
    for indx in range(0, len(standard.client_bind) - 1):
        bite = read_file(standard.client_bind[indx], standard.client_bind[indx + 1])
        await sock.send(bite)
        await asyncio.sleep(0)
        yield sha256(bite).hexdigest(), len(bite)


async def collect_contents(sock: WebSocketClientProtocol) -> Generator[Tuple[bytes, int], None, None]:
    """
    Collect contents from target client and save them to intended file

    :param sock: Websocket object belonging to the server session
    :return: Tuple of file contents and contents length
    """
    for _ in range(standard.client_chks - 1):
        mesgcont = await sock.recv()
        if isinstance(mesgcont, bytes):
            fuse_file(mesgcont)
            await asyncio.sleep(0)
            yield sha256(mesgcont).hexdigest(), len(mesgcont) - 16


async def deliver_digest_checks(sock: WebSocketClientProtocol) -> bool:
    """
    Inform target client with message digest of file contents

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    general("Delivering contents digest for confirmation.")
    await sock.send(dumps({"call": "hash", "data": standard.client_hash.hexdigest()}))
    return True


async def collect_digest_checks() -> bool:
    """
    Show textual message with message digest of file contents

    :return: Confirmation of the action completion
    """
    general("Collecting contents digest for confirmation.")
    return True


async def deliver_confirmation(sock: WebSocketClientProtocol, data: str = standard.client_hash.hexdigest()) -> bool:
    """
    Inform target client of the file contents integrity confirmation

    :param sock: Websocket object belonging to the server session
    :param data: Message digest from the file contents exchanged
    :return:
    """
    standard.client_movestop = time.time()
    if data == standard.client_hash.hexdigest():
        general(f"Contents integrity verified (Mean {ease_size(standard.client_filesize / (standard.client_movestop - standard.client_movestrt))}/s).")
        await sock.send(dumps({"call": "conf", "data": 1}))
        return True
    else:
        general(f"Contents integrity mismatch (Mean {ease_size(standard.client_filesize / (standard.client_movestop - standard.client_movestrt))}/s).")
        await sock.send(dumps({"call": "conf", "data": 0}))
        return False


async def collect_confirmation(data: int = 0) -> bool:
    """
    Show textual message of the file contents integrity confirmation

    :param data: Confirmation of the message digest comparison
    :return: Confirmation of the action completion
    """
    standard.client_movestop = time.time()
    if bool(data):
        general(f"Contents integrity verified (Mean {ease_size(standard.client_filesize / (standard.client_movestop - standard.client_movestrt))}/s).")
        return True
    else:
        general(f"Contents integrity mismatch (Mean {ease_size(standard.client_filesize / (standard.client_movestop - standard.client_movestrt))}/s).")
        return False


async def deliver_separation_from_mistaken_password(sock: WebSocketClientProtocol) -> bool:
    """
    Inform target client of disconnection due to mistaken password

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    general("Delivering status update on mistaken password.")
    await sock.send(dumps({"call": "flub"}))
    return True


async def collect_separation_from_mistaken_password() -> bool:
    """
    Show textual message of disconnection due to mistaken password

    :return: Confirmation of the action completion
    """
    general("Collecting status update on mistaken password.")
    return True
