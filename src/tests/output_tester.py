from sys import stdout

if __name__ == "__main__":
    for n in range(1, 165):
        stdout.write("test" * n + "\n")
    stdout.flush()
