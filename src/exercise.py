"""
This module manages the loading of exercise related information.
"""

import json
import os

from typing import Any, Dict, List

SPEC_TYPE = Dict[str, Any]

REQUIRED_FILES: List[str] = [
    "json",  # exercise specifications
    "py",  # test case generation
    "txt",  # exercise description
]

REQUIRED_SPECS: List[str] = [
    "exercise",
    "judge",
    "time_limit",
    "memory_limit",
    "testcases",
]

SPEC_FORMATTING: Dict[str, str] = {
    "time_limit": "{key}: {value} s",
    "memory_limit": "{key}: {value} MiB",
}


def exists(path: str, ex_name: str) -> bool:
    """
    Determine whether the exercise `ex_name` exists in the directory
    `path`.

    :param path: a string; the directory in which the supposed exercise
        is located.
    :param ex_name: a string; the name of the supposed exercise.
    :return: a boolean; `True` if the exercise exists.
    """

    for file_ext in REQUIRED_FILES:
        ex_path = os.path.join(path, f"{ex_name}.{file_ext}")
        if not os.path.isfile(ex_path):
            return False
    return True


def get_description(path: str, ex_name: str) -> str:
    """
    Get the exercise description of the exercise `ex_name` located in
    the directory `path`.

    :param path: a string; the directory in which the exercise is
        located.
    :param ex_name: a string; the name of the exercise.
    :return: a string; the description (along with the specifications)
        of the exercise.
    """

    if not exists(path, ex_name):
        raise AssertionError(f"the exercise `{ex_name}` does not exist")

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
    with open(desc_path, "r") as fd:
        return_str += fd.read()

    return return_str


def get_specs(path: str, ex_name: str) -> SPEC_TYPE:
    """
    Get the exercise specifications of the exercise `ex_name` located
    in the directory `path`.

    :param path: a string; the directory in which the exercise is
        located.
    :param ex_name: a string; the name of the exercise.
    :return: `SPEC_TYPE`; a dictionary with each of its keys
        being the name of a specification.

            ex: {"judge": "default", "time_limit": 2.0, ... }
    """

    if not exists(path, ex_name):
        raise AssertionError(f"the exercise `{ex_name}` does not exist")

    desc_path: str = os.path.join(path, f"{ex_name}.json")

    try:
        with open(desc_path, "r") as fd:
            specs: SPEC_TYPE = json.load(fd)

        for spec_name in REQUIRED_SPECS:
            if spec_name not in specs:
                raise AssertionError

        return specs

    except (json.JSONDecodeError, AssertionError):
        raise AssertionError(f"the file `{desc_path}` is corrupt; please generate it again")


def list_exercises(path: str) -> List[str]:
    """
    Get the names of all the exercises found in the directory `path`.

    :param path: a string; the directory in which to look for
        exercises.
    :return: a list of strings; the names of all the exercises located
        in the directory `path`.
    """

    if not os.path.isdir(path):
        raise AssertionError(f"the exercises location `{path}` is not a directory")

    all_names = frozenset(f.split(".")[0] for f in os.listdir(path))

    return [ex_name for ex_name in all_names if exists(path, ex_name)]
