import typing


def float_judge(program_output: typing.List[str], expected_output: typing.List[str],
                precision: int = 8) -> bool:
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
