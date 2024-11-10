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


from json import dumps
from uuid import uuid4

from websockets.legacy.server import WebSocketServerProtocol

from expedite.config import standard
from expedite.server.base import ExpediteConnection
from expedite.view import failure, general, success, warning


async def exchange_insert(sock: WebSocketServerProtocol, plan: str = standard.client_plan, scan: str = standard.client_endo, time: int = standard.client_time) -> str | bool:
    """
    Comply with the client request of joining the network

    If client ABC joins before client XYZ
      - assuming that client ABC wants to connect to client XYZ
      - client ABC does not need to provide any target identity
      - client XYZ has to provide client ABC as target identity

    :param sock: Websocket object belonging to the connecting client
    :param plan: Operation intent of the connecting client - This can be either SEND or RECV depending on the purpose
    :param scan: Target client sought by the connecting client - This can be either empty string or hexadecimal string
    :param time: Identity provided by the exchange server to the connecting client to be recognized within the network
    :return: Confirmation of the action completion
    """
    if sock not in standard.connection_dict:
        if plan in ["SEND", "RECV"]:
            iden = uuid4().hex[0:8].upper()
            standard.connection_dict[sock] = ExpediteConnection(iden, plan, scan, time)
            if plan == "SEND":
                warning(f"{iden} joined with the intention of delivering.")
            elif plan == "RECV":
                warning(f"{iden} joined with the intention of collecting.")
            if scan == "":
                general(f"{iden} is waiting for client for {time} seconds.")
            else:
                general(f"{iden} is looking for {scan} for {time} seconds.")
            await sock.send(dumps({"call": "okay", "iden": iden}))
            return iden
        else:
            return False
    else:
        return False


async def exchange_remove(sock: WebSocketServerProtocol) -> bool:
    """
    Inform the client about them being booted off the network

    Here is how the logic works -

    Once participant ABC is flagged for removal either from client side or server side
      - If participant ABC exists in the connection dictionary
        - If participant ABC is paired with participant XYZ
          - Participant XYZ is disconnected from the network and removed from the connection dictionary
          - Participant ABC is disconnected from the network and removed from the connection dictionary
        - If participant ABC is not paired with anyone else
          - Participant ABC is disconnected from the network and removed from the connection dictionary
      - If participant ABC does not exist in the connection dictionary
        - Do nothing

    :param sock: Websocket object belonging to the disconnecting client
    :return: Confirmation of the action completion
    """
    if sock in standard.connection_dict:
        if standard.connection_dict[sock].ptsc in standard.connection_dict and standard.connection_dict[sock].ptsc.state == 1:
            warning(f"{standard.connection_dict[sock].ptid} left.")
            await standard.connection_dict[sock].ptsc.close(code=1000)
            standard.connection_dict.pop(standard.connection_dict[sock].ptsc)
        warning(f"{standard.connection_dict[sock].iden} left.")
        await sock.close(code=1000)
        standard.connection_dict.pop(sock)
        return True
    else:
        return False


async def exchange_inform(sock: WebSocketServerProtocol, plan: str = standard.client_plan, scan: str = standard.client_endo, iden: str = standard.client_iden) -> int:
    """
    Inform the client about them being able to join the network

    Here is how the logic works -

    After client ABC is able to join the network with operation intent P
      - If client ABC has provided that they are looking for client XYZ for DEF seconds
        - If client XYZ has not yet joined the network
          - Client ABC will wait until the client XYZ will join the network [Code 3]
          - Client ABC will disconnect after DEF seconds if the client XYZ does not turn up
        - If client XYZ has been connected to the network for a while
          - If client XYZ is not yet paired with anyone else
            - If client XYZ has the operation intent Q (opposite of operation intent P of client ABC)
              - Client ABC will be paired with client XYZ due to the positive operation intents [Code 0]
              - Client XYZ will be paired with client ABC due to the positive operation intents [Code 0]
            - If client XYZ has the operation intent P (selfsame of operation intent P of client ABC)
              - Client ABC will be booted off the network due to the negative operation intents [Code 1]
              - Client XYZ will be booted off the network due to the negative operation intents [Code 1]
          - If client XYZ has already paired with anyone else
            - Client ABC will be booted off the network as client XYZ is already paired [Code 2]
      - If client ABC has provided that they are waiting for connection for DEF seconds
        - Client ABC will wait until they are connected with some client [Code 3]
        - Client ABC will disconnect after DEF seconds if they are not paired until then

    :param sock: Websocket object belonging to the connecting client
    :param plan: Operation intent of the connecting client - This can be either SEND or RECV depending on the purpose
    :param scan: Target client sought by the connecting client - This can be either empty string or hexadecimal string
    :param iden: Identity provided by the exchange server to the connecting client to be recognized within the network
    :return: Confirmation of the action completion
    """
    for indx in standard.connection_dict:
        if standard.connection_dict[indx].iden == scan:
            if not standard.connection_dict[indx].ptsc:
                if plan != standard.connection_dict[indx].plan:
                    success(f"{iden} and {scan} are positively paired.")
                    await indx.send(dumps({"call": "note", "part": iden}))
                    await sock.send(dumps({"call": "note", "part": scan}))
                    standard.connection_dict[indx].pair_connection(iden, sock)
                    standard.connection_dict[sock].pair_connection(scan, indx)
                    return 0
                else:
                    failure(f"{iden} and {scan} are negatively paired.")
                    await indx.send(dumps({"call": "awry", "part": iden}))
                    await sock.send(dumps({"call": "awry", "part": scan}))
                    return 1
            else:
                failure(f"{iden} and {scan} cannot pair as {scan} is already paired.")
                await sock.send(dumps({"call": "lone", "part": scan}))
                return 2
    return 3


async def exchange_json(sock: WebSocketServerProtocol, note: str = "", data: str = "") -> bool:
    """
    Convey the JSON elements from delivering client to collecting client

    :param sock: Websocket object belonging to the delivering client
    :param note: Action requested to be performed by the collecting client
    :param data: Data elements that are to be conveyed across
    :return: Confirmation of the action completion
    """
    general(standard.server_note[note].format(sj=standard.connection_dict[sock].iden, oj=standard.connection_dict[sock].ptid))
    if sock in standard.connection_dict:
        if standard.connection_dict[sock].ptsc in standard.connection_dict and standard.connection_dict[sock].ptsc.state == 1:
            await standard.connection_dict[sock].ptsc.send(data)
            return True
        else:
            return False
    else:
        return False


async def exchange_byte(sock: WebSocketServerProtocol, pack: bytes = b"") -> bool:
    """
    Convey the file contents from delivering client to collecting client

    :param sock: Websocket object belonging to the delivering client
    :param pack: File contents that are to be conveyed across
    :return: Confirmation of the action completion
    """
    if sock in standard.connection_dict:
        if standard.connection_dict[sock].ptsc in standard.connection_dict and standard.connection_dict[sock].ptsc.state == 1:
            await standard.connection_dict[sock].ptsc.send(pack)
            return True
        else:
            general(f"{standard.connection_dict[sock].iden} could not deliver contents to {standard.connection_dict[sock].ptid} as {standard.connection_dict[sock].ptid} is no longer connected.")
            return False
    else:
        general("Attempting for aborting connection.")
        return False
