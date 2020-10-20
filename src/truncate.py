"""
This module manages the truncation of messages for a cleaner output.
"""

from typing import List, Optional

# a large number to represent no limit
INFINITY: int = (1 << 64) - 1

# the message to display when something has been truncated
TRUNCATED_STRING: str = "⯇truncated⯈"


def truncate(
        s: List[str],
        char_limit: Optional[int] = None,
        nl_limit: Optional[int] = None
) -> List[str]:
    """
    Truncate a given string to either `char_limit` characters or
    `nl_limit` lines, using the more limiting one.

    :param List[str] s:
        The message to truncate (each string in the list represents one
        line of a program's output).

    :param int char_limit:
        The maximum number of characters in the truncated string.

    :param int nl_limit:
        The maximum number of newlines in the truncated string.

    :return List[str]:
        The output string, with a maximum of `char_limit` characters
        and `nl_limit` lines.
    """

    if char_limit is None and nl_limit is None:
        return s

    char_limit = INFINITY if char_limit is None else char_limit
    nl_limit = INFINITY if nl_limit is None else nl_limit

    return_s: List[str] = []
    for i, line in enumerate(s):
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

        if not char_limit and i + 1 < len(s):
            return_s.append(TRUNCATED_STRING)
            break

    return return_s
