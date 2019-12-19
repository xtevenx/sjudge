import argparse
import json
import os
import sys

import judge

EXERCISES_LOCATION = "tests/"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test your programs.")
    parser.add_argument(
        "exercise_name", action="store",  nargs="?", type=str,
        help="the name of the exercise to test your program for.")
    parser.add_argument(
        "program_path", action="store",  nargs="?", type=str,
        help="the path to the program to test.")
    arguments = parser.parse_args()

    if arguments.exercise_name is None or arguments.program_path is None:
        parser.print_help()
        sys.exit(0)

    exercise_test_path = os.path.join(
        EXERCISES_LOCATION, f"{arguments.exercise_name}.json")
    if not os.path.exists(exercise_test_path):
        print(f"error: exercise `{arguments.exercise_name}` does not exist.")
        sys.exit(0)

    if not os.path.exists(arguments.program_path):
        print(f"error: program `{arguments.program_path}` does not exist.")
        sys.exit(0)

    judge.judge_file(
        arguments.program_path,
        json.load(open(exercise_test_path, "r"))
    )
