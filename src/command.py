"""
This module contains a function for getting the command to run a file
based on the its extension.
"""

import platform
import shlex
import subprocess

from typing import Dict, Tuple

# the result of `platform.system()` on Windows 10
WINDOWS: str = "Windows"

# a dictionary with supported programming languages and their
# respective commands for running:
#     {extensions: (unix_command, windows_command)}
LANGUAGES: Dict[frozenset, Tuple[str, str]] = {
    frozenset({"jar"}): ("java -jar {}",) * 2,
    frozenset({"js"}): ("node {}",) * 2,
    frozenset({"py", "pyc"}): ("python3 {}", "python {}"),
}

# default command to run a file
DEFAULT_COMMAND: str = "./{}"


def _exists(c: str) -> bool:
    """
    Test whether the command `c` exists by running `f"{c} --version"`.

    :param c: a string; the command to check for existence.
    :return: a boolean; `True` if the command exists.
    """

    try:
        r = subprocess.run(
            shlex.split(f"{c} --version"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

    return r.returncode == 0


def get_command(f: str) -> str:
    """
    Get the command to run a file based on its file extension.

    :param f: a string; the name of the file of which to get the
        command.
    :return: a string; the command to run the file.
    """

    ext = f.split(".")[-1]
    for language_ext, commands in LANGUAGES.items():
        if ext in language_ext:
            full_c = commands[platform.system() == WINDOWS].format(f)

            # note: convert next two lines to use walrus operator when
            # Python 3.7 support is dropped.
            c = full_c.split()[0]
            if not _exists(c):
                raise AssertionError(f"the command `{c}` does not exist")
            return full_c
    return DEFAULT_COMMAND.replace("{}", f)
