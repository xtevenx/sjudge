"""
This module contains the 'float' judge. This judge expects all the
program's outputs to be numbers (usually floats). It does not test for
the program's output to be exactly the reference output; it checks if
it is numerically close enough to the reference output.
"""

from typing import Sequence


def float_judge(program_output: Sequence[str], expected_output: Sequence[str], precision: int = 8
                ) -> bool:
    """
    Judge a program's output based on the 'float' judge.

    :param program_output: the program's output.
    :param expected_output: the reference output.
    :param precision: the number of decimals to count before the rest
        is considered noise. For example, if the precision is 2 and the
        reference output is "3.14", then "3.138" and "3.141 would be
        correct but "3.132" and "3.147" would be incorrect.
    :return: `True` if the program's output is correct.
    """

    if len(program_output) != len(expected_output):
        return False

    try:
        for line_i, program_line in enumerate(program_output):
            program_line = program_line.split()
            expected_line = expected_output[line_i].split()

            if len(program_line) != len(expected_line):
                return False

            for i, number in enumerate(program_line):
                number = round(float(number), precision)
                if round(float(expected_line[i]), precision) != number:
                    return False
    except ValueError:
        return False

    return True
