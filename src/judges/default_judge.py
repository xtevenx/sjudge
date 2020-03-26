"""
This module contains the 'default' judge. This judge strips all
whitespace at the starts and ends of the program's output lines before
checking if it identical to the reference output.
"""

from typing import Sequence

STRIP_VALUES: str = "".join([' ', '\t'])


def default_judge(program_output: Sequence[str], expected_output: Sequence[str]) -> bool:
    """
    Judge a program's output based on the 'default' judge.

    :param program_output: the program's output.
    :param expected_output: the reference output.
    :return: `True` if the program's output is correct.
    """

    if len(program_output) != len(expected_output):
        return False

    return all(s.strip(STRIP_VALUES) == expected_output[i].strip(STRIP_VALUES)
               for i, s in enumerate(program_output))
