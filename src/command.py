"""
This module manages getting the command to run a file based on the its
extension.
"""

import platform
import typing

# the result of `platform.system()` on Windows 10
WINDOWS: str = "Windows"

# a dictionary with supported programming languages and their
# respective commands for running:
#     {extensions: (unix_command, windows_command)}
LANGUAGES: typing.Dict[frozenset, typing.Tuple[str, str]] = {
    frozenset({"py", "pyc"}): ("python3 {}", "python {}"),
    frozenset({"jar"}): ("java -jar {}",) * 2,
}

# default command to run a file
DEFAULT_COMMAND: str = "./{}"


def get_command(f: str) -> str:
    """
    Get the command to run a file based on its file extension.
    :param f: name of the file of which to get the command
    :return: command to run the file
    """

    ext = f.split(".")[-1]
    for language_ext, commands in LANGUAGES.items():
        if ext in language_ext:
            return commands[platform.system() == WINDOWS].format(f)
    return DEFAULT_COMMAND.replace("{}", f)
