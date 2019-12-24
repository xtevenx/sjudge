import typing

STRIP_VALUES: str = "".join([' ', '\t'])


def default_judge(program_output: typing.List[str],
                  expected_output: typing.List[str]) -> bool:
    if len(program_output) != len(expected_output):
        return False

    return all(
        s.strip(STRIP_VALUES) == expected_output[i]
        for i, s in enumerate(program_output)
    )
