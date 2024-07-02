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


import os
from json import dumps, loads
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from expedite.client.excp import PasswordMistaken

from expedite.config import standard


def derive_code(password: str = standard.client_pswd, salt: bytes = standard.client_salt) -> bytes:
    kdfo = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    return kdfo.derive(password.encode())


def encr_bite(data: bytes = b"", code: bytes = standard.client_code, invc: bytes = standard.client_invc) -> bytes:
    cipher = Cipher(algorithms.AES(code), modes.CBC(invc), backend=default_backend())
    encrob = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    paddat = padder.update(data) + padder.finalize()
    return encrob.update(paddat) + encrob.finalize()


def decr_bite(data: bytes = b"", code: bytes = standard.client_code, invc: bytes = standard.client_invc) -> bytes:
    try:
        cipher = Cipher(algorithms.AES(code), modes.CBC(invc), backend=default_backend())
        decrob = cipher.decryptor()
        ucrper = padding.PKCS7(algorithms.AES.block_size).unpadder()
        ucrdat = decrob.update(data) + decrob.finalize()
        return ucrper.update(ucrdat) + ucrper.finalize()
    except ValueError:
        raise PasswordMistaken


def encr_metadata() -> bytes:
    standard.client_invc, standard.client_salt = os.urandom(16), os.urandom(16)
    data = dumps({"call": "meta", "name": standard.client_filename, "size": standard.client_filesize, "chks": len(standard.client_bind)-1})
    standard.client_code = derive_code(standard.client_pswd, standard.client_salt)
    endt = encr_bite(data.encode(encoding="utf-8"), standard.client_code, standard.client_invc)
    standard.client_metadone = True
    return standard.client_invc + standard.client_salt + endt


def decr_metadata(pack: bytes = b"") -> tuple:
    standard.client_invc, standard.client_salt = pack[0:16], pack[16:32]
    data = pack[32:]
    standard.client_code = derive_code(standard.client_pswd, standard.client_salt)
    dedt = loads(decr_bite(data, standard.client_code, standard.client_invc).decode(encoding="utf-8"))
    standard.client_metadone = True
    return dedt["name"], dedt["size"], dedt["chks"]
