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


from asyncio import run

from expedite.client.room import oper

from click import IntRange, option, version_option, group, Path

from expedite import __versdata__
from expedite.config import standard
from expedite.client.meet import talk
from expedite.view import failure, warning

import sys


def work():
    try:
        run(oper())
    except OSError as expt:
        warning(f"{expt}")
        failure("Exiting.")
        sys.exit(1)


@group(
    name="expedite",
    context_settings={"show_default": True},
)
@option(
    "-a",
    "--addr",
    "addr",
    type=str,
    default=standard.client_addr,
    required=True,
    help="Set the address for the service endpoint"
)
@option(
    "-t",
    "--time",
    "time",
    type=IntRange(5, 30),
    default=standard.client_time,
    required=False,
    help="Set the expiry period for participants"
)
@option(
    "-e",
    "--endo",
    "endo",
    type=str,
    default=standard.client_endo,
    required=False,
    help="Set the identity of the opposing client"
)
@version_option(
    version=__versdata__, prog_name="Expedite Client by Akashdeep Dhar"
)
def main(
    addr: str = standard.client_addr,
    time: int = standard.client_time,
    endo: str = standard.client_endo,
):
    standard.client_addr = addr
    standard.client_time = time
    standard.client_endo = endo


@main.command(
    name="send",
    help="Deliver file through an encrypted transfer",
    context_settings={"show_default": True},
)
@option(
    "-p",
    "--pswd",
    "pswd",
    type=str,
    default=standard.client_pswd,
    help="Set the password for delivering encryption",
)
@option(
    "-f",
    "--file",
    "file",
    type=Path(exists=True),
    required=True,
    help="Set the filepath for delivering to network",
)
def send(
    pswd: str = standard.client_pswd,
    file: str = standard.client_file
) -> None:
    try:
        standard.client_pass = pswd
        standard.client_file = file
        standard.client_plan = "SEND"
        talk()
        work()
    except KeyboardInterrupt:
        failure("Exiting.")
        sys.exit(1)


@main.command(
    name="recv",
    help="Collect file through an encrypted transfer",
    context_settings={"show_default": True},
)
@option(
    "-p",
    "--pswd",
    "pswd",
    type=str,
    required=True,
    help="Set the password for collecting encryption"
)
def recv(
    pswd: str = standard.client_pswd
) -> None:
    try:
        standard.client_pswd = pswd
        standard.client_plan = "RECV"
        talk()
        work()
    except KeyboardInterrupt:
        failure("Exiting.")
        sys.exit(1)
