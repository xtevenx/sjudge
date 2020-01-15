"""
This module contains the 'default' judge. This judge strips all
whitespace at the starts and ends of the program's output lines before
checking if it identical to the reference output.
"""

import typing

STRIP_VALUES: str = "".join([' ', '\t'])


def default_judge(program_output: typing.List[str], expected_output: typing.List[str]) -> bool:
    """
    Judge a program's output based on the 'default' judge.

    :param program_output: a sequence of strings; the program's output.
    :param expected_output: a sequence of strings; the reference
        output.
    :return: a boolean; `True` if the program's output is correct.
    """

    if len(program_output) != len(expected_output):
        return False

    return all(s.strip(STRIP_VALUES) == expected_output[i].strip(STRIP_VALUES)
               for i, s in enumerate(program_output))
