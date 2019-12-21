import argparse
import json
import os
import sys

import judge
import exercise

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
    parser.add_argument(
        "-l", "--list_exercises", action="store_true",
        help="display a list of all the exercise names.",
        dest="list_exercises")
    arguments = parser.parse_args()

    if arguments.list_exercises:
        lessons_list = exercise.get_exercises_list(EXERCISES_LOCATION)
        lessons_list = [f"  - {lesson_name}" for lesson_name in lessons_list]

        print(f"Found {len(lessons_list)} lessons:")
        print("\n".join(lessons_list))
        sys.exit(0)

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
