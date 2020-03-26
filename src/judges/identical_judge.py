"""
This module contains the 'identical' judge. This judge directly checks
if the program's output is identical to the reference answer.
"""

from typing import Sequence


def identical_judge(program_output: Sequence[str], expected_output: Sequence[str]) -> bool:
    """
    Judge a program's output based on the 'identical' judge.

    :param program_output: the program's output.
    :param expected_output: strings; the reference output.
    :return: `True` if the program's output is correct.
    """

    if len(program_output) != len(expected_output):
        return False

    return all(s == expected_output[i] for i, s in enumerate(program_output))
