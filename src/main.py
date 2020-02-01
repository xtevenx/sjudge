import argparse
import os
import sys
import traceback

import command
import display
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
        help="display a list of all the exercises.", dest="list_exercises")
    parser.add_argument(
        "-s", "--see_description", action="store_true",
        help="display the description for the given exercise.", dest="see_description")
    parser.add_argument(
        "-e", "--exercises_location", action="store", default=DEFAULT_EXERCISES,
        help="set the base directory of the exercises.", dest="exercises_location")
    parser.add_argument(
        "-m", "--manual_command", action="store_true",
        help="enable this flag if you are entering the full command to run your program under "
             "`program_path` (instead of just the file name).", dest="manual_command")
    parser.add_argument(
        "-q", "--quiet", action="count", default=0,
        help="use this flag if you want the program to run with less output. can be applied up to "
             "two times.", dest="quiet")
    arguments = parser.parse_args()

    if arguments.list_exercises:
        lessons_list = exercise.list_exercises(arguments.exercises_location)
        lessons_list = [f"  ⮡ {lesson_name}" for lesson_name in lessons_list]

        display.display(f"Found {len(lessons_list)} lessons:")
        display.display("\n".join(lessons_list))
        sys.exit(0)

    if arguments.see_description:
        if arguments.exercise_name is None:
            raise AssertionError("no exercise name was specified")

        display.display(exercise.get_description(
            arguments.exercises_location, arguments.exercise_name
        ))
        sys.exit(0)

    if arguments.exercise_name is None or arguments.program_path is None:
        parser.print_help()

        missing_value = "exercise_name" if arguments.exercise_name is None else "program_path"
        raise AssertionError(f"the argument `{missing_value}` is missing")

    program_command = arguments.program_path
    if not arguments.manual_command:
        if not os.path.isfile(arguments.program_path):
            raise AssertionError(f"the file `{arguments.program_path}` does not exist")
        program_command = command.get_command(arguments.program_path)

    display.set_verbosity(arguments.quiet)

    judge.judge_program(
        program_command,
        **exercise.get_specs(arguments.exercises_location, arguments.exercise_name)
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as err:
        print(f"error: {err.args[0]}.")
    except KeyboardInterrupt:
        print("stopping judging due to user interrupt.")
    except SystemExit as err:
        sys.exit(*err.args)
    except Exception as err:
        print("<-- ERROR TRACEBACK -->")
        traceback.print_tb(err.__traceback__)
        print("  " + err.__repr__())

        print("an unexpected error has occurred; if you believe this is a bug, please \n"
              "report it with the full error message.")
        sys.exit(1)
