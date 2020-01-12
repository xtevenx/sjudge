"""
This module manages the truncation of messages for cleaner display.
"""

import typing

# a large number to represent no limit
INFINITY: int = (1 << 64) - 1

# the message to display when something has been truncated
TRUNCATED_STRING: str = "⯇truncated⯈"


def truncate(s: typing.List[str], char_limit: typing.Optional[int] = None,
             nl_limit: typing.Optional[int] = None) -> typing.List[str]:
    """
    Truncate a string based on a given character and newline limit.
    :param s: string to truncate
    :param char_limit: maximum characters in the truncated string
    :param nl_limit: maximum newlines in the truncated string
    :return: truncated string (based on `char_limit` and `nl_limit`)
    """

    if char_limit is None and nl_limit is None:
        return s

    char_limit = INFINITY if char_limit is None else char_limit
    nl_limit = INFINITY if nl_limit is None else nl_limit

    return_s: typing.List[str] = []
    for line in s:
        if len(line) > char_limit:
            return_s.append(line[:char_limit])
            return_s.append(TRUNCATED_STRING)
            break
        elif nl_limit <= 0:
            return_s.append(TRUNCATED_STRING)
            break

        return_s.append(line)
        char_limit -= len(line)
        nl_limit -= 1

    return return_s
