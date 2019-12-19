import json
import random

TESTCASES: int = 100

X_RANGE: iter = range(10 ** 9)
Y_RANGE: iter = range(1, 10 ** 9)
Y_RANGE_SMALL: iter = range(1, 10 ** 3)

if __name__ == "__main__":
    tests = []

    for _ in range(TESTCASES - 1):
        x = random.choice(X_RANGE)
        y = random.choice(
            Y_RANGE if random.random() < 0.1 else Y_RANGE_SMALL
        )
        tests.append([[str(x), str(y)], [str(x // y)]])
    tests.append([["0", random.choice(Y_RANGE)], ["0"]])

    json.dump(tests, open("divide.json", "w+"))
