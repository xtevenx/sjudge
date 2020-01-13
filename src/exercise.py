"""
This module manages the loading of exercise details.
"""

import json
import os
import typing

SPEC_TYPE: typing.Type = typing.Dict[str, typing.Any]

REQUIRED_FILES: typing.List[str] = [
    "json",  # exercise specifications
    "py",  # test case generation
    "txt",  # exercise description
]

REQUIRED_SPECS: typing.List[str] = [
    "exercise",
    "judge",
    "time_limit",
    "memory_limit",
    "testcases",
]

SPEC_FORMATTING: typing.Dict[str, str] = {
    "time_limit": "{key}: {value} s",
    "memory_limit": "{key}: {value} MiB",
}


def get_description(path: str, ex_name: str) -> str:
    """
    Get the exercise description of `ex_name` located in `path`. This
    also gets the specifications from the ".json" file.
    :param path: the directory of the exercise
    :param ex_name: the name of the exercise
    :return: the description (along with the specs)
    """

    return_str = ""

    for key, value in get_specs(path, ex_name).items():
        if key == "testcases":
            continue

        formatted_key = key.replace("_", " ").capitalize()

        try:
            return_str += SPEC_FORMATTING[key].format(key=formatted_key, value=value) + "\n"
        except KeyError:
            return_str += f"{formatted_key}: {value}\n"

    return_str += "\n"

    desc_path = os.path.join(path, f"{ex_name}.txt")
    if not os.path.isfile(desc_path):
        raise AssertionError(f"the exercise `{ex_name}` does not exist")

    with open(desc_path, "r") as fd:
        return_str += fd.read()

    return return_str


def get_specs(path: str, ex_name: str) -> SPEC_TYPE:
    """
    Get the exercise specifications of `ex_name` located in `path`.
    :param path: the directory of the exercise
    :param ex_name: the name of the exercise
    :return: the specifications
    """

    desc_path: str = os.path.join(path, f"{ex_name}.json")
    if not os.path.isfile(desc_path):
        raise AssertionError(f"the exercise `{ex_name}` does not exist")

    try:
        with open(desc_path, "r") as fd:
            specs: SPEC_TYPE = json.load(fd)

        for spec_name in REQUIRED_SPECS:
            if spec_name not in specs:
                raise AssertionError

        return specs

    except (json.JSONDecodeError, AssertionError):
        raise AssertionError(f"the file `{desc_path}` is corrupt; please generate it again")


def list_exercises(path: str) -> typing.List[str]:
    """
    Get the names of all the exercises found in `path`.
    :param path: the directory of the exercises
    :return: names of all the exercises
    """

    if not os.path.isdir(path):
        raise AssertionError(f"the exercises location `{path}` is not a directory")

    found_lessons: typing.List[str] = []
    all_names = frozenset(f.split(".")[0] for f in os.listdir(path))

    for ex_name in all_names:
        for file_ext in REQUIRED_FILES:
            ex_path = os.path.join(path, f"{ex_name}.{file_ext}")
            if not os.path.isfile(ex_path):
                break
        else:
            found_lessons.append(ex_name)

    return found_lessons
