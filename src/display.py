"""
This module manages the logging/displaying of information.
"""

import sys
import typing

# characters to use when console doesn't support Unicode
SIMPLE_CHARACTERS: typing.Dict[str, str] = {
    "⮡": "\\>",
    "→": "->",
    "⯇": "<",
    "⯈": ">",
}

# global variables to set the program's level of verbosity
ALL: int = 0
RESULT_ONLY: int = 1
SUMMARY_ONLY: int = 2
_VERBOSITY: int = ALL


def display(s: str = "", v: int = ALL) -> None:
    """
    Write `s` to standard output. Simplifies Unicode characters if
    they are not supported by the console.

    :param s: the string to write to standard output.
    :param v: an integer; the level of verbosity of the message.
    """

    if _VERBOSITY > v:
        return

    try:
        sys.stdout.write(f"{s}\n")
    except UnicodeEncodeError:
        for old, new in SIMPLE_CHARACTERS.items():
            s = s.replace(old, new)
        sys.stdout.write(f"{s}\n")

    sys.stdout.flush()


def set_verbosity(level: int = ALL) -> None:
    """
    Set the program's level of verbosity.

    :param level: an integer; the level of verbosity at which to set
        the program.
    """

    global _VERBOSITY
    _VERBOSITY = level
