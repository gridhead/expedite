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
from asyncio import run

from click import IntRange, Path, group, option, version_option
from websockets.exceptions import InvalidURI

from expedite import __versdata__
from expedite.client.base import bite_file, find_name, find_size
from expedite.client.meet import talk
from expedite.client.prompt.room import oper
from expedite.client.prompt.util import facade_exit
from expedite.config import standard


def work() -> None:
    """
    Start the worker module to start the transfer service

    :return:
    """
    talk()
    try:
        run(oper())
    except OSError:
        run(facade_exit(None, False, "oser"))
        sys.exit(standard.client_exit)
    except InvalidURI:
        run(facade_exit(None, False, "iuri"))
        sys.exit(standard.client_exit)
    except KeyboardInterrupt:
        run(facade_exit(None, False, "intr"))
        sys.exit(standard.client_exit)


@group(
    name="expedite",
    context_settings={"show_default": True},
)
@option(
    "-h",
    "--host",
    "host",
    type=str,
    default=standard.client_host,
    required=True,
    help="Set the address for the service endpoint"
)
@option(
    "-t",
    "--time",
    "time",
    type=IntRange(5, 300),
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
    version=__versdata__, prog_name="Expedite Prompt by Akashdeep Dhar"
)
def main(
    host: str = standard.client_host,
    time: int = standard.client_time,
    endo: str = standard.client_endo,
) -> None:
    """
    Configure the service particulars before starting it

    :param host: Location where the exchange service is hosted
    :param time: Time for which the client has to wait before disconnecting
    :param endo: Network identity of target client for pairing and transfer
    :return:
    """
    standard.client_host = host
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
@option(
    "-s",
    "--size",
    "size",
    type=IntRange(1024, 524288, clamp=True),
    default=standard.chunking_size,
    help="Set the unit size for file chunking (in B)",
)
def send(
    pswd: str = standard.client_pswd,
    file: str = standard.client_file,
    size: int = standard.chunking_size,
) -> None:
    """
    Configure the service particulars before delivering

    :param pswd: Password for encrypting purposes
    :param file: Filepath for delivering file
    :param size: Unit size for file chunking
    :return:
    """
    standard.client_pswd = pswd
    standard.client_file = file
    standard.chunking_size = size
    standard.client_filesize = find_size()
    standard.client_filename = find_name()
    standard.client_bind = bite_file()
    standard.client_plan = "SEND"
    work()


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
    """
    Configure the service particulars before collecting

    :param pswd: Password for decrypting purposes
    :return:
    """
    standard.client_pswd = pswd
    standard.client_plan = "RECV"
    work()


if __name__ == "__main__":
    main()
