import argparse
import json
import os
import sys
import traceback

import command
import exercise
import judge

DEFAULT_EXERCISES = "exercises/"


def main():
    parser = argparse.ArgumentParser(description="Test your programs.")
    parser.add_argument(
        "exercise_name", action="store", nargs="?", type=str,
        help="the name of the exercise to test your program for.")
    parser.add_argument(
        "program_path", action="store", nargs="?", type=str,
        help="the path to the program to test.")
    parser.add_argument(
        "-l", "--list_exercises", action="store_true",
        help="display a list of all the exercise names.", dest="list_exercises")
    parser.add_argument(
        "-s", "--see_description", action="store_true",
        help="display the description for the given exercise.", dest="see_description")
    parser.add_argument(
        "-e", "--exercises_location", action="store",
        help="set the location of the exercises.", dest="exercises_location")
    arguments = parser.parse_args()

    exercises_location = (
        arguments.exercises_location if arguments.exercises_location is not None
        else DEFAULT_EXERCISES
    )

    if arguments.list_exercises:
        lessons_list = exercise.get_exercises_list(exercises_location)
        lessons_list = [f"  - {lesson_name}" for lesson_name in lessons_list]

        print(f"Found {len(lessons_list)} lessons:")
        print("\n".join(lessons_list))
        sys.exit(0)

    if arguments.see_description:
        if arguments.exercise_name is None:
            print("error: no exercise name specified")
        else:
            try:
                print(exercise.get_exercise_description(
                    exercises_location, arguments.exercise_name
                ))
            except FileNotFoundError:
                print(f"error: exercise `{arguments.exercise_name}` does not exist.")

        sys.exit(0)

    if arguments.exercise_name is None or arguments.program_path is None:
        parser.print_help()
        sys.exit(0)

    exercise_test_path = os.path.join(exercises_location, f"{arguments.exercise_name}.json")
    if not os.path.exists(exercise_test_path):
        print(f"error: exercise `{arguments.exercise_name}` does not exist.")
        sys.exit(0)

    if not os.path.exists(arguments.program_path):
        print(f"error: program `{arguments.program_path}` does not exist.")
        sys.exit(0)

    judge.judge_file(
        command.get_run_command(arguments.program_path),
        **json.load(open(exercise_test_path, "r"))
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit as err:
        sys.exit(*err.args)
    except KeyboardInterrupt:
        print("Detected `KeyboardInterrupt()`, stopping judging.")
    except AssertionError as err:
        full_error = "\n".join(err.args)
        print(f"Detected error: `{full_error}`; this should not be a bug (please check your "
              f"configurations).")
    except BaseException as err:
        print("<-- ERROR TRACEBACK -->")
        traceback.print_tb(err.__traceback__)
        print("  " + err.__repr__())

        print("Error detected; if you believe this is a bug, please report it with the full\n"
              "error message.")
        sys.exit(1)
