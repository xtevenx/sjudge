import json
import os
import typing

from random import choice
from math import floor, sqrt

# The "input/output format" for the testing data is a list of strings.
# Each string in the list represents a line of characters that is to be
# passed to the tested program.
IO_TYPE = typing.List[str]

# The format of a test is a tuple of two "input/output format" lists.
# The first represents the input that is given to the tested program
# and the second represents the expected output from the program.
TEST_TYPE = typing.Tuple[IO_TYPE, IO_TYPE]

# Set the name of the exercise for which to generate testing data (this
# file should be called EXERCISE_NAME.py).
EXERCISE_NAME: str = os.path.basename(__file__[:-3])

# define all required exercise specifications.
EXERCISE_SPECIFICATIONS: typing.Dict[str, typing.Any] = {
    "exercise": EXERCISE_NAME,
    "judge": "default",
    "time_limit": 1.0,
    "memory_limit": 32,
}

# set the number of testcases for the exercise to have.
TESTCASES_PER_X_RANGE: int = 10
SQUARE_TESTCASES: int = 9

# `X` is each input in the test case.
X_RANGES: iter = [
    range(2, 10 ** 3),
    range(10 ** 3, 10 ** 6),
    range(10 ** 6, 10 ** 9),
    range(10 ** 9, 10 ** 12)
]


# define solution function
def num_factors(x):
    if x == 0:
        return "inf"

    factors = 0
    for f in range(1, floor(sqrt(x)) + 1):
        q, r = divmod(x, f)
        if r == 0:
            factors += 1 + (q != f)
    return str(factors)


if __name__ == "__main__":
    tests: typing.List[TEST_TYPE] = []

    for x_range in X_RANGES:
        for _ in range(TESTCASES_PER_X_RANGE):
            x_value = choice(x_range)
            tests.append((
                [str(x_value)], [num_factors(x_value)]
            ))

    tests.append((
        ["0"], ["inf"]
    ))

    for _ in range(SQUARE_TESTCASES):
        x_value = choice(range(1, 10 ** 6)) ** 2
        tests.append((
            [str(x_value)], [num_factors(x_value)]
        ))

    EXERCISE_SPECIFICATIONS["testcases"] = tests

    # save the exercise information.
    json.dump(EXERCISE_SPECIFICATIONS, open(f"{EXERCISE_NAME}.json", "w+"))
