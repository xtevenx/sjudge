from math import floor, sqrt

x: int = int(input())

if x == 0:
    print("inf")
else:
    factors = 0
    for f in range(1, floor(sqrt(x)) + 1):
        q, r = divmod(x, f)
        if r == 0:
            factors += 1 + (q != f)
    print(factors)
