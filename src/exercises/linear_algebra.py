import json
import os
import random
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
EXERCISE_NAME: str = os.path.basename(__file__[:-3])

# define all required exercise specifications.
EXERCISE_SPECIFICATIONS: typing.Dict[str, typing.Any] = {
    "exercise": EXERCISE_NAME,
    "judge": "default",
    "time_limit": 10.0,
    "memory_limit": 256,
}

# set the number of testcases for the exercise to have.
TESTCASES_PER_N: int = 4

# `N` is conventionally the number of inputs in the test case.
N_RANGE: iter = range(1, 16)

# `X` is each input in the test case.
X_RANGE: iter = range(-(1 << 7), 1 << 7)

if __name__ == "__main__":
    tests: typing.List[TEST_TYPE] = []

    for N in N_RANGE:
        for _ in range(TESTCASES_PER_N):
            solutions = random.sample(X_RANGE, N)
            coefficients = [random.sample(X_RANGE, N) for _ in range(N)]

            if 0 not in solutions and random.random() < (1 / TESTCASES_PER_N):
                solutions[random.randrange(N)] = 0

            answers = [0 for _ in range(N)]
            for eq_i, eq_c in enumerate(coefficients):
                for c_i, c in enumerate(eq_c):
                    answers[eq_i] += c * solutions[c_i]

            tests.append((
                [
                    str(N),
                    " ".join(" ".join(map(str, c)) for c in coefficients),
                    " ".join(map(str, answers))
                ], [str(s) for s in solutions]
            ))

    EXERCISE_SPECIFICATIONS["testcases"] = tests

    # save the exercise information.
    json.dump(EXERCISE_SPECIFICATIONS, open(f"{EXERCISE_NAME}.json", "w+"))
