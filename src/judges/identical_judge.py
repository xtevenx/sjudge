import typing


def identical_judge(program_output: typing.List[str],
                    expected_output: typing.List[str]) -> bool:
    if len(program_output) != len(expected_output):
        return False

    return all(s == expected_output[i] for i, s in enumerate(program_output))
