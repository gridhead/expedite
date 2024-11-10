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


from os.path import basename, exists, getsize

from expedite.client.auth import decr_bite, encr_bite
from expedite.config import standard


def find_size() -> int:
    """
    Retrieve the file size using the file location

    :return: Size of the intended file
    """
    return getsize(standard.client_file)


def find_name() -> str:
    """
    Retrieve the file name using the file location

    :return: Name of the intended file
    """
    return basename(standard.client_file)


def ease_size(size: int | float) -> str:
    """
    Retrieve the file size in human-readable format

    :param size: Size in byte count format
    :return: Size in human-readable format
    """
    unitlist = ["B", "KB", "MB", "GB", "TB", "PB"]
    indx, opsz = 0, size
    if size == 0:
        return "0.00B"
    else:
        while opsz >= 1024 and indx < len(unitlist) - 1:
            opsz, indx = opsz / 1024.0, indx + 1
        return f"{opsz:.2f}{unitlist[indx]}"


def bite_file() -> list:
    """
    Retrieve the list of read ranges from chunk size

    :return: List of read ranges
    """
    init, size, bite = 0, standard.client_filesize, []
    while init < size:
        bite.append(init)
        if size - init >= standard.chunking_size:
            init = init + standard.chunking_size
        else:
            bite.append(size)
            init = size
    return bite


def read_file(init: int = 0, fina: int = 0) -> bytes:
    """
    Retrieve the chunk from the provided byte range

    :param init: Starting byte index for reading
    :param fina: Stopping byte index for reading
    :return: Chunks to read
    """
    if exists(standard.client_file):
        with open(standard.client_file, "rb") as file:
            file.seek(init)
            data = file.read(fina - init)
            endt = encr_bite(data, standard.client_code, standard.client_invc)
            standard.client_hash.update(data)
        return endt
    else:
        return b""


def fuse_file(pack: bytes = b"") -> bool:
    """
    Create and join the chunks on the storage device

    :param pack: Chunks to save
    :return:
    """
    if not standard.client_fileinit:
        mode, standard.client_fileinit = "wb", True
    else:
        mode = "ab"
    with open(standard.client_filename, mode) as file:
        dedt = decr_bite(pack, standard.client_code, standard.client_invc)
        file.write(dedt)
        standard.client_hash.update(dedt)
    return True
