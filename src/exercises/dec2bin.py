import json
import random
import typing

# The "input/output format" for the testing data is a list of strings.
# Each string in the list represents a line of characters that is to be
# passed to the tested program.
IO_TYPE: typing.Type = typing.List[str]

# The format of a test is a tuple of two "input/output format" lists.
# The first represents the input that is given to the tested program
# and the second represents the expected output from the program.
TEST_TYPE: typing.Type = typing.Tuple[IO_TYPE, IO_TYPE]

# Set the name of the exercise for which to generate testing data (this
# file should be called EXERCISE_NAME.py).
EXERCISE_NAME: str = __file__[:-3]

# define all required exercise specifications.
EXERCISE_SPECIFICATIONS: typing.Dict[str, typing.Any] = {
    "exercise": EXERCISE_NAME,
    "judge": "default",
    "time_limit": 0.5,
    "memory_limit": 64,
}

# set the number of testcases for the exercise to have.
T_RANGE: iter = range(int(10 ** 2), 5 * int(10 ** 3) + 1, int(10 ** 2))

# `N` is conventionally the number of inputs in the test case.
N_RANGE: iter = range(1, 65)

if __name__ == "__main__":
    tests: typing.List[TEST_TYPE] = []

    for T in T_RANGE:
        test_input: IO_TYPE = [str(T)]
        test_output: IO_TYPE = []
        for _ in range(T):
            N = random.choice(N_RANGE)
            X = random.randrange(1 << (N - 1), 1 << N)
            test_input.append(bin(X)[2:])
            test_output.append(str(X))
        tests.append((test_input, test_output))

    EXERCISE_SPECIFICATIONS["testcases"] = tests

    # save the exercise information.
    json.dump(EXERCISE_SPECIFICATIONS, open(f"{EXERCISE_NAME}.json", "w+"))
