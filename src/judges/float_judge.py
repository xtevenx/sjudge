import typing


def float_judge(program_output: typing.List[str], expected_output: typing.List[str],
                precision: int = 8) -> bool:
    if len(program_output) != len(expected_output):
        return False

    for i, program_line in enumerate(program_output):
        if len(program_line.split()) != len(expected_output[i].split()):
            return False

    try:
        for line_i, program_line in enumerate(program_output):
            expected: typing.List[str] = expected_output[line_i].split()
            for i, number in enumerate(program_line.split()):
                number = round(float(number), precision)
                if round(float(expected[i]), precision) != number:
                    return False
    except ValueError:
        return False

    return True
