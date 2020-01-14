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


def display(s: str = "") -> None:
    """
    Write `s` to standard output. Simplifies Unicode characters if
    they are not supported by the console.

    :param s: the string to write to standard output.
    """

    try:
        sys.stdout.write(f"{s}\n")
    except UnicodeEncodeError:
        for old, new in SIMPLE_CHARACTERS.items():
            s = s.replace(old, new)
        sys.stdout.write(f"{s}\n")

    sys.stdout.flush()
