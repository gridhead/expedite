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


from websockets.legacy.server import WebSocketServerProtocol

from expedite.config import standard


class ExpediteConnection:
    def __init__(self, iden: str = standard.client_iden, plan: str = standard.client_plan, scan: str = standard.client_endo, time: int = standard.client_time) -> None:
        """
        Initialize the Expedite connection with the client identity, operation intent, target identity and waiting time

        :param iden: Identity provided by the exchange server to the connecting client to be recognized within the network
        :param plan: Operation intent of the connecting client - This can be either SEND or RECV depending on the purpose
        :param scan: Target client sought by the connecting client - This can be either empty string or hexadecimal string
        :param time: Time for which a connecting client will stay connected to the network and wait for a pairing process
        :return:
        """
        self.iden = iden
        self.plan = plan
        self.scan = scan if scan != "" else None
        self.time = time
        self.ptid = ""
        self.ptsc = None

    def pair_connection(self, ptid: str = standard.client_endo, ptsc: WebSocketServerProtocol = None) -> None:
        """
        Configure the partner identity and partner sought when the pairing process with both the clients has completed

        These attributes belong to the pairmate and are populated for the client after the pairing process is complete

        :param ptid: Identity provided by the exchange server to the connecting client to be recognized within the network
        :param ptsc: Websocket object belonging to the connecting client
        :return:
        """
        self.ptid = ptid
        self.ptsc = ptsc
