import json
import typing

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
EXERCISE_NAME: str = __file__[:-3]

# define all required exercise specifications.
EXERCISE_SPECIFICATIONS: typing.Dict[str, typing.Any] = {
    "exercise": EXERCISE_NAME,
    "judge": "default",
    "time_limit": 1.0,
    "memory_limit": 256,
}

# set the number of testcases for the exercise to have.
TESTCASES: int = 100

# `N` is conventionally the number of inputs in the test case.
N_RANGE: iter = range(1, int(10 ** 5))

# `X` is each input in the test case.
X_RANGE: iter = range(-(10 ** 9), 10 ** 9)

if __name__ == "__main__":
    tests: typing.List[TEST_TYPE] = []

    for _ in range(TESTCASES):
        # Generate the exercise testcases here and store them in
        # `tests`. `tests` is a list of tests which represents the test
        # cases to test the tested program on.
        pass

    EXERCISE_SPECIFICATIONS["testcases"] = tests

    # save the exercise information.
    json.dump(EXERCISE_SPECIFICATIONS, open(f"{EXERCISE_NAME}.json", "w+"))
