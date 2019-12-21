LANGUAGE_EXTENSIONS = {
    frozenset({"py", "pyc"}): "python3 {}",
    frozenset({"jar"}): "java -jar {}",
}

BASE_COMMAND = "./{}"


def get_run_command(filename: str) -> str:
    extension: str = filename.split(".")[-1]
    for extensions, command in LANGUAGE_EXTENSIONS.items():
        if extension in extensions:
            return command.format(filename)
    return BASE_COMMAND.format(filename)
