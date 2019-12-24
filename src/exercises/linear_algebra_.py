import json
import random

TESTCASES_PER_N: int = 5

N_RANGE: iter = range(1, 13)
X_RANGE: iter = range(-(1 << 7), 1 << 7)

if __name__ == "__main__":
    tests = []

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

            tests.append([
                [
                    str(N),
                    " ".join(" ".join(map(str, c)) for c in coefficients),
                    " ".join(map(str, answers))
                ], [str(s) for s in solutions]
            ])

    json.dump(tests, open("linear_algebra.json", "w+"))