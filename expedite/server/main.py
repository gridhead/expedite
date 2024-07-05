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
from asyncio import get_event_loop

from click import IntRange, command, option, version_option
from websockets import serve

from expedite import __versdata__
from expedite.config import standard
from expedite.server.meet import talk
from expedite.server.room import oper
from expedite.view import failure, general


def work():
    func = serve(oper, standard.server_addr, standard.server_port)
    get_event_loop().run_until_complete(func)
    get_event_loop().run_forever()


@command(
    name="expedite",
    context_settings={"show_default": True},
)
@option(
    "-a",
    "--addr",
    "addr",
    type=str,
    default=standard.server_addr,
    required=False,
    help="Set the interface for the service endpoint"
)
@option(
    "-p",
    "--port",
    "port",
    type=IntRange(min=64, max=65535),
    default=standard.server_port,
    required=False,
    help="Set the port value for the service endpoint"
)
@version_option(
    version=__versdata__, prog_name="Expedite Server by Akashdeep Dhar"
)
def main(addr: str = standard.server_addr, port: int = standard.server_port) -> None:
    try:
        standard.server_addr = addr
        standard.server_port = port
        talk()
        work()
    except KeyboardInterrupt:
        failure("Interrupt received.")
        general("Exiting.")
        sys.exit(1)
    except OSError:
        failure("Port occupied.")
        general("Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
