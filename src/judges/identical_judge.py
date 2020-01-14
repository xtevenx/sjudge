"""
This module contains the 'identical' judge. This judge directly checks
if the program's output is identical to the reference answer.
"""

import typing


def identical_judge(program_output: typing.List[str], expected_output: typing.List[str]) -> bool:
    """
    Judge a program's output based on the 'identical' judge.

    :param program_output: a sequence of strings; the program's output.
    :param expected_output: a sequence of strings; the reference
        output.
    :return: a boolean; `True` if the program's output is correct.
    """

    if len(program_output) != len(expected_output):
        return False

    return all(s == expected_output[i] for i, s in enumerate(program_output))
