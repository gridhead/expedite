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
from hashlib import sha256
from logging import getLogger
from logging.config import dictConfig
from uuid import uuid4

server_addr = "127.0.0.1"
server_port = 8080

server_note = {
    "meta": "{sj} is attempting to share file metadata to {oj}.",
    "drop": "{sj} is attempting to fetch file contents from {oj}.",
    "hash": "{sj} is delivering digest to {oj}.",
    "conf": "{sj} is delivering confirmation to {oj}.",
    "flub": "{sj} has received mistaken password from {oj}.",
}

client_host = ""
client_time = 150
client_pswd = uuid4().hex[0:8].upper()
client_plan = ""
client_endo = ""
client_file = ""
client_iden = ""
client_pair = False
client_bind = []
client_comp = 0
client_hash = sha256()
client_exit = 1
client_strt = time.time()
client_chks = 0

client_filename = ""
client_filesize = 0
client_fileinit = False
client_saltsize = 16
client_movestrt = 0
client_movestop = 0
client_salt = b""
client_invc = b""
client_code = b""
client_metadone = False
client_progress = False

chunking_size = 1024 * 64

connection_dict = dict()
connection_list = set()

testdict = dict()

client_note = {
    "awry": "Mismatch interactions.",
    "lone": "Hitherto paired.",
    "dprt": "Node disconnected.",
    "intr": "Interrupt received.",
    "oser": "Connection failed.",
    "iuri": "Mistaken URI.",
    "rest": "Expiry achieved.",
    "flub": "Mistaken password.",
    "succ": "Operation complete.",
    "fail": "Operation failed."
}

client_text = {
    "awry": "Interaction cannot proceed further as the both clients have requested for the identical actions from each other. Please try again while ensuring that both clients have requested dissimilar actions this time.",
    "lone": "Interaction cannot proceed further as the client that was requested to be connected to is already connected with a different client. Please try again while ensuring that the client is not already connected.",
    "dprt": "Interaction cannot proceed further as the client has disconnected from the broker server. Please ensure that the interaction remains stable in your next attempt by requesting for a decreased processing size.",
    "intr": "Interaction cannot proceed further as the client has been requested to cancel the ongoing task. Please initiate the interaction again using the interface if the interaction had been aborted unintentionally.",
    "oser": "Interaction cannot proceed further as the client cannot connect reliably to the broker server using the provided broker server URI. Please try again after ensuring that the broker server is working properly.",
    "iuri": "Interaction cannot proceed further as the client cannot connect reliably to the broker server using the provided broker server URI. Please try again to start interaction after revising the broker server URI.",
    "rest": "Interaction cannot proceed further as the client has timed out waiting for pairing. Please consider increasing the expiry time for participants and requesting the other client to connect as soon as possible.",
    "flub": "Interaction cannot proceed further as the client has been provided with a mistaken password. Please try again while confirming that the correct password is provided at both delivering and collecting clients.",
    "succ": "Contents integrity verified.<br/><br/>The client <b>{iden}</b> has succeeded to {verb} file contents {drct} client <b>{endo}</b>.<br/><br/><b>File name.</b> {name}<br/><b>File size.</b> {size}<br/><b>SHA256 sum.</b> {hash}<br/><b>Duration.</b> {time}<br/><b>Mean speed.</b> {spid}",
    "fail": "Contents integrity mismatch.<br/><br/>The client <b>{iden}</b> has failed to {verb} file contents {drct} client <b>{endo}</b>.<br/><br/><b>File name.</b> {name}<br/><b>File size.</b> {size}<br/><b>SHA256 sum.</b> {hash}<br/><b>Duration.</b> {time}<br/><b>Mean speed.</b> {spid}",
}

logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

dictConfig(logrconf)

logger = getLogger(__name__)
