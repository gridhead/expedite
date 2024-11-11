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


def success(text) -> None:
    """
    Show textual message in success format

    :param text: Textual message
    :return:
    """
    standard.logger.info(style(text, fg="green", bold=True))


def failure(text) -> None:
    """
    Show textual message in failure format

    :param text: Textual message
    :return:
    """
    standard.logger.error(style(text, fg="red", bold=True))


def warning(text) -> None:
    """
    Show textual message in warning format

    :param text: Textual message
    :return:
    """
    standard.logger.warning(style(text, fg="yellow", bold=True))


def general(text) -> None:
    """
    Show textual message in general format

    :param text: Textual message
    :return:
    """
    standard.logger.info(text)
