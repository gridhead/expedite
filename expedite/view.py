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


from click import style

from expedite.config import standard


def success(message) -> None:
    standard.logger.info(style(message, fg="green", bold=True))


def failure(message) -> None:
    standard.logger.error(style(message, fg="red", bold=True))


def warning(message) -> None:
    standard.logger.warning(style(message, fg="yellow", bold=True))


def general(message) -> None:
    standard.logger.info(message)
