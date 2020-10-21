"""
This module contains a function for getting the command to run a file
based on the its extension.
"""

import platform
import shlex
import subprocess

from typing import Dict

# The result of `platform.system()` on Windows 10.
WINDOWS: str = "Windows"

# A dictionary with programming language extensions as keys and their
# respective commands for running in a tuple as values. If there is two
# commands in the value, the first one if for unix-like systems and the
# second one is for windows based systems.
LANGUAGES: Dict[frozenset, tuple] = {
    frozenset({"jar"}): ("java -jar {}",),
    frozenset({"js"}): ("node {}",),
    frozenset({"py", "pyc"}): ("python3 {}", "python {}"),
}

# The default command to run a file (if no language-specific command
# was found).
DEFAULT_COMMAND: str = "./{}"

# See `_exists()` for more information.
_CHECK_TIMEOUT: int = 1


def _exists(c: str) -> bool:
    """
    Check whether the command `c` exists by running it with the
    "--version" argument in the command line and seeing whether the
    exit code is zero.
    """

    try:
        r = subprocess.run(
            shlex.split(f"{c} --version"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=_CHECK_TIMEOUT
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

    return r.returncode == 0


def get_command(f: str) -> str:
    """
    Get the command to run the file `f` based on its file extension.
    """

    ext = f.split(".")[-1]
    for extensions, commands in LANGUAGES.items():
        if ext in extensions:
            # Gets the last value of `commands` if we are on Windows,
            # otherwise get the first value. If there is only one
            # command for both systems (`commands` contains only one
            # value), the last value will be the first value.
            full_c = commands[-(platform.system() == WINDOWS)].format(f)

            # Note: convert next two lines to use walrus operator when
            # Python 3.7 support is dropped (just to be annoying).
            c = full_c.split()[0]
            if not _exists(c):
                raise AssertionError(f"the command `{c}` does not exist")

            return full_c

    return DEFAULT_COMMAND.replace("{}", f)
