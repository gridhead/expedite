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


import sys
import time
from asyncio import ensure_future, get_event_loop
from datetime import datetime
from json import loads

from tqdm.asyncio import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from websockets import connect
from websockets.exceptions import ConnectionClosed
from websockets.legacy.client import WebSocketClientProtocol

from expedite.client.base import ease_size, fuse_file
from expedite.client.conn import (
    collect_confirmation,
    collect_connection_from_pairness,
    collect_connection_to_server,
    collect_contents,
    collect_digest_checks,
    collect_dropping_summon,
    collect_metadata,
    collect_separation_from_mistaken_password,
    deliver_confirmation,
    deliver_connection_to_server,
    deliver_contents,
    deliver_digest_checks,
    deliver_dropping_summon,
    deliver_metadata,
    deliver_separation_from_mistaken_password,
)
from expedite.client.prompt.util import deliver_suspension_from_expiry_prompt, facade_exit
from expedite.config import standard
from expedite.view import general


async def oper() -> None:
    """
    Exchange data to the target client after connecting to the exchange server

    :return:
    """
    try:
        async with connect(standard.client_host) as sock:
            get_event_loop().call_later(standard.client_time, lambda: ensure_future(deliver_suspension_from_expiry_prompt(sock)))
            await deliver_connection_to_server(sock)
            async for mesgcont in sock:
                if isinstance(mesgcont, str):
                    mesgdict = loads(mesgcont)
                    # If the data received is of STRING type
                    if standard.client_plan in ["SEND", "RECV"]:
                        # If the purpose of the client is either DELIVERING or COLLECTING
                        if mesgdict["call"] == "okay":
                            await collect_connection_to_server(mesgdict["iden"])
                        elif mesgdict["call"] in ["awry", "lone"]:
                            await facade_exit(sock, False, mesgdict["call"])
                    if standard.client_plan == "SEND":
                        # If the purpose of the client is DELIVERING
                        if mesgdict["call"] == "note":
                            await collect_connection_from_pairness(mesgdict["part"])
                            await deliver_metadata(sock)
                        elif mesgdict["call"] == "conf":
                            complete = await collect_confirmation(mesgdict["data"])
                            await facade_exit(sock, complete, "done" if complete else "dprt")
                        elif mesgdict["call"] == "flub":
                            await collect_separation_from_mistaken_password()
                            await facade_exit(sock, False, "flub")
                        elif mesgdict["call"] == "drop":
                            await collect_dropping_summon()
                            await show_deliver_contents(sock)
                            await deliver_digest_checks(sock)
                    else:
                        # If the purpose of the client is COLLECTING
                        if mesgdict["call"] == "note":
                            await collect_connection_from_pairness(mesgdict["part"])
                        elif mesgdict["call"] == "hash":
                            await collect_digest_checks()
                            complete = await deliver_confirmation(sock, mesgdict["data"])
                            await facade_exit(sock, complete, "done" if complete else "dprt")
                else:
                    # If the data received is of BYTES type
                    if standard.client_plan == "RECV":
                        # If the purpose of the client is COLLECTING
                        if not standard.client_metadone:
                            if await collect_metadata(mesgcont):
                                await deliver_dropping_summon(sock)
                            else:
                                await deliver_separation_from_mistaken_password(sock)
                                await facade_exit(sock, False, "flub")
                        else:
                            await show_collect_contents(sock, mesgcont)
            sys.exit(standard.client_exit)
    except ConnectionClosed:
        await facade_exit(sock, False, "dprt")
        sys.exit(standard.client_exit)


async def show_deliver_contents(sock: WebSocketClientProtocol) -> bool:
    """
    Facilitate encrypting and delivering file contents

    :param sock: Websocket object belonging to the server session
    :return: Confirmation of the action completion
    """
    general(f"Delivering contents for '{standard.client_filename}' ({ease_size(standard.client_filesize)}) to {standard.client_endo}.")
    standard.client_movestrt = time.time()
    with logging_redirect_tqdm():
        with tqdm(total=standard.client_filesize, unit="B", unit_scale=True, unit_divisor=1024, leave=False, initial=0) as prog:
            async for dgst, size in deliver_contents(sock):
                prog.set_description(f"{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} SHA256 {dgst}")
                prog.update(size)
    return True


async def show_collect_contents(sock: WebSocketClientProtocol, pack: bytes = b"") -> bool:
    """
    Facilitate collecting and decrypting file contents

    :param sock: Websocket object belonging to the server session
    :param pack: Byte chunk that is to be collected and decrypted
    :return: Confirmation of the action completion
    """
    general(f"Collecting contents for '{standard.client_filename}' ({ease_size(standard.client_filesize)}) from {standard.client_endo}.")
    standard.client_movestrt = time.time()
    fuse_file(pack)
    with logging_redirect_tqdm():
        with tqdm(total=standard.client_filesize, unit="B", unit_scale=True, unit_divisor=1024, leave=False, initial=len(pack)) as prog:
            async for dgst, size in collect_contents(sock):
                prog.set_description(f"{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} SHA256 {dgst}")
                prog.update(size)
    return True
