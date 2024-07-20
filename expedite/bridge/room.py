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


import time
from asyncio import ensure_future, get_event_loop, sleep
from hashlib import sha256
from json import dumps, loads
from pathlib import Path

from PySide6.QtWidgets import QMessageBox
from websockets import connect
from websockets.exceptions import ConnectionClosed, InvalidURI

from expedite.bridge.base import truncate_text
from expedite.client.base import ease_size, fuse_file, read_file
from expedite.client.conn import (
    collect_confirmation,
    collect_connection_from_pairness,
    collect_digest_checks,
    collect_dropping_summon,
    collect_metadata,
    collect_permission_to_join,
    collect_separation_from_mistaken_password,
    deliver_confirmation,
    deliver_connection_to_server,
    deliver_digest_checks,
    deliver_dropping_summon,
    deliver_metadata,
    deliver_separation_from_mistaken_password,
)
from expedite.config import standard
from expedite.view import general, warning


class Connection:
    def __init__(self):
        self.sock = None

    async def maintain_connection(self):
        try:
            async with connect(standard.client_host) as self.sock:
                get_event_loop().call_later(standard.client_time, lambda: ensure_future(self.suspension_from_expiry()))
                await deliver_connection_to_server(self.sock)
                async for mesgcont in self.sock:
                    if isinstance(mesgcont, str):
                        mesgdict = loads(mesgcont)
                        # If the data received is of STRING type
                        if standard.client_plan in ["SEND", "RECV"]:
                            # If the purpose of the client is either DELIVERING or COLLECTING
                            if mesgdict["call"] == "okay":
                                await collect_permission_to_join(mesgdict["iden"])
                                self.ui.statarea.showMessage("Please share your acquired identity to begin interaction")
                                self.ui.identity.setText(f"{mesgdict["iden"]}")
                            elif mesgdict["call"] in ["awry", "lone"]:
                                await self.sock.close()
                                warning(standard.client_note[mesgdict["call"]])
                                self.show_dialog(QMessageBox.Critical, standard.client_note[mesgdict["call"]], standard.client_text[mesgdict["call"]])
                        if standard.client_plan == "SEND":
                            # If the purpose of the client is DELIVERING
                            if mesgdict["call"] == "note":
                                await collect_connection_from_pairness(mesgdict["part"])
                                self.ui.statarea.showMessage(f"You are now paired with {mesgdict["part"]}")
                                standard.client_endo = mesgdict["part"]
                                await deliver_metadata(self.sock)
                            elif mesgdict["call"] == "conf":
                                complete = await collect_confirmation(mesgdict["data"])
                                await self.sock.close()
                                standard.client_movestop = time.time()
                                head = standard.client_note["succ"] if complete else standard.client_note["fail"]
                                text = standard.client_text["succ"] if complete else standard.client_text["fail"]
                                self.show_dialog(
                                    QMessageBox.Information,
                                    head,
                                    text.format(
                                        iden=standard.client_iden,
                                        verb="deliver",
                                        drct="to",
                                        endo=standard.client_endo,
                                        name=standard.client_filename,
                                        size=ease_size(standard.client_filesize),
                                        hash=standard.client_hash.hexdigest(),
                                        time=f"{(standard.client_movestop - standard.client_movestrt):.2f} seconds",
                                        spid=f"{ease_size(0)}/s",
                                    )
                                )
                            elif mesgdict["call"] == "flub":
                                await collect_separation_from_mistaken_password()
                                await self.sock.close()
                                warning(standard.client_note[mesgdict["call"]])
                                self.show_dialog(
                                    QMessageBox.Critical,
                                    standard.client_note[mesgdict["call"]],
                                    standard.client_text[mesgdict["call"]]
                                )
                            elif mesgdict["call"] == "drop":
                                await collect_dropping_summon()
                                self.ui.statarea.showMessage(f"File contents are requested by {standard.client_endo}")
                                await self.deliver_contents()
                                await deliver_digest_checks(self.sock)
                        else:
                            # If the purpose of the client is COLLECTING
                            if mesgdict["call"] == "note":
                                await collect_connection_from_pairness(mesgdict["part"])
                                self.ui.statarea.showMessage(f"You are now paired with {mesgdict["part"]}")
                                standard.client_endo = mesgdict["part"]
                            elif mesgdict["call"] == "hash":
                                await collect_digest_checks()
                                complete = await deliver_confirmation(self.sock, mesgdict["data"])
                                await self.sock.close()
                                standard.client_movestop = time.time()
                                head = standard.client_note["succ"] if complete else standard.client_note["fail"]
                                text = standard.client_text["succ"] if complete else standard.client_text["fail"]
                                self.show_dialog(
                                    QMessageBox.Information,
                                    head,
                                    text.format(
                                        iden=standard.client_iden,
                                        verb="collect",
                                        drct="from",
                                        endo=standard.client_endo,
                                        name=standard.client_filename,
                                        size=ease_size(standard.client_filesize),
                                        hash=standard.client_hash.hexdigest(),
                                        time=f"{(standard.client_movestop - standard.client_movestrt):.2f} seconds",
                                        spid=f"{ease_size(0)}/s",
                                    )
                                )
                    else:
                        # If the data received is of BYTES type
                        if standard.client_plan == "RECV":
                            # If the purpose of the client is COLLECTING
                            if not standard.client_metadone:
                                if await collect_metadata(mesgcont):
                                    self.ui.clct_head_file.setText(f"Collecting <b>{truncate_text(standard.client_filename, 28)}</b> ({ease_size(standard.client_filesize)})")
                                    standard.client_filename = Path(standard.client_file) / Path(standard.client_filename)
                                    await deliver_dropping_summon(self.sock)
                                else:
                                    await deliver_separation_from_mistaken_password(self.sock)
                                    await self.sock.close()
                                    warning(standard.client_note["flub"])
                                    self.show_dialog(QMessageBox.Critical, standard.client_note["flub"], standard.client_text["flub"])
                            else:
                                await self.collect_contents(mesgcont)
        except InvalidURI:
            self.show_dialog(QMessageBox.Critical, standard.client_note["iuri"], standard.client_text["iuri"])
        except OSError:
            self.show_dialog(QMessageBox.Critical, standard.client_note["oser"], standard.client_text["oser"])
        except ConnectionClosed:
            self.show_dialog(QMessageBox.Critical, standard.client_note["dprt"], standard.client_text["dprt"])
        self.normal_both_side()
        standard.client_progress = False

    async def deliver_contents(self):
        standard.client_movestrt = time.time()
        for indx in range(0, len(standard.client_bind) - 1):
            bite = read_file(standard.client_bind[indx], standard.client_bind[indx + 1])
            self.ui.progbarg.setValue(indx * 100 / (len(standard.client_bind) - 1))
            self.ui.statarea.showMessage(f"[{standard.client_endo}] Since {(time.time() - standard.client_movestrt):.2f} seconds | SHA256 {sha256(bite).hexdigest()[0:4]} ({ease_size(len(bite))})")
            await self.sock.send(bite)
            await sleep(0)
        self.ui.progbarg.setValue(100)

    async def collect_contents(self, pack):
        standard.client_movestrt = time.time()
        fuse_file(pack)
        for indx in range(0, standard.client_chks - 1):
            cont = await self.sock.recv()
            if isinstance(cont, bytes):
                fuse_file(cont)
                self.ui.progbarg.setValue(indx * 100 / (standard.client_chks))
                self.ui.statarea.showMessage(f"[{standard.client_endo}] Since {(time.time() - standard.client_movestrt):.2f} seconds | SHA256 {sha256(cont).hexdigest()[0:4]} ({ease_size(len(cont))})")
                await sleep(0)
        self.ui.progbarg.setValue(100)

    async def suspension_from_expiry(self):
        if not standard.client_pair:
            general("Attempting to abandon from the network after expiry.")
            await self.sock.send(dumps({"call": "rest"}))
            await self.sock.close()
            warning(standard.client_note["rest"])
            self.show_dialog(QMessageBox.Warning, standard.client_note["rest"], standard.client_text["rest"])
