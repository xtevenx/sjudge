import platform
import typing

WINDOWS: str = "Windows"

LANGUAGE_EXTENSIONS: typing.Dict[frozenset, typing.Callable[[str], str]] = {
    frozenset({"py", "pyc"}): lambda s: "python {}" if s == WINDOWS else "python3 {}",
    frozenset({"jar"}): lambda s: "java -jar {}",
}

BASE_COMMAND: str = "./{}"


def get_run_command(filename: str) -> str:
    extension = filename.split(".")[-1]
    for extensions, command in LANGUAGE_EXTENSIONS.items():
        if extension in extensions:
            command_string = command(platform.system())
            return command_string.replace("{}", filename)
    return BASE_COMMAND.replace("{}", filename)
