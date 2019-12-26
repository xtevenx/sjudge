import typing

INFINITY: int = (1 << 31) - 1
TRUNCATED_STRING: str = "<output truncated>"


def truncate(s: typing.List[str], character_limit: typing.Optional[int],
             newline_limit: typing.Optional[int]) -> typing.List[str]:
    if character_limit is None and newline_limit is None:
        return s

    character_limit = INFINITY if character_limit is None else character_limit
    newline_limit = INFINITY if newline_limit is None else newline_limit

    return_s: typing.List[str] = []
    for i, line in enumerate(s):
        if len(line) > character_limit:
            return_s.append(line[:character_limit])
            return_s.append(TRUNCATED_STRING)
            break
        elif newline_limit <= 0:
            return_s.append(TRUNCATED_STRING)
            break
        else:
            return_s.append(line)
            character_limit -= len(line)
            newline_limit -= 1

    return return_s
