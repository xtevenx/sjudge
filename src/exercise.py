"""
This module manages the loading and management of exercise related
information.
"""

import json
import os

from typing import Any, Dict, List

SPEC_TYPE = Dict[str, Any]

_REQUIRED_FILES: List[str] = [
    "json",  # exercise specifications
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
    """

    for file_ext in _REQUIRED_FILES:
        ex_path = os.path.join(path, f"{ex_name}.{file_ext}")
        if not os.path.isfile(ex_path):
            return False
    return True


def get_description(path: str, ex_name: str) -> str:
    """
    Get the description of the exercise `ex_name` located in the
    directory `path`.
    """

    if not exists(path, ex_name):
        raise AssertionError(f"the exercise `{ex_name}` does not exist")

    return_str = ""

    for key, value in get_specs(path, ex_name).items():
        if key == "testcases":
            continue

        formatted_key = key.replace("_", " ").capitalize()

        try:
            return_str += SPEC_FORMATTING[key].format(
                key=formatted_key, value=value
            )
        except KeyError:
            return_str += f"{formatted_key}: {value}"
        return_str += "\n"

    return_str += "\n"

    desc_path = os.path.join(path, f"{ex_name}.txt")
    with open(desc_path, "r") as fd:
        return_str += fd.read()

    return return_str


def get_specs(path: str, ex_name: str) -> SPEC_TYPE:
    """
    Get the exercise specifications of the exercise `ex_name` located
    in the directory `path`.

    :return SPEC_TYPE:
        A dictionary with its keys being the names of different
        attributes of the exercise.
            ex: {"judge": "default", "time_limit": 2.0, ... }
    """

    if not exists(path, ex_name):
        raise AssertionError(f"the exercise `{ex_name}` does not exist")

    spec_path: str = os.path.join(path, f"{ex_name}.json")

    try:
        with open(spec_path, "r") as fd:
            specs: SPEC_TYPE = json.load(fd)

        for spec_name in REQUIRED_SPECS:
            if spec_name not in specs:
                raise AssertionError

        return specs

    except (json.JSONDecodeError, AssertionError):
        raise AssertionError(
            f"the file `{spec_path}` is corrupt."
        )


def list_exercises(path: str) -> List[str]:
    """
    Get the names of all the exercises found in the directory `path`.
    """

    if not os.path.isdir(path):
        raise AssertionError(
            f"the exercises location `{path}` is not a directory"
        )

    all_names = frozenset(f.split(".")[0] for f in os.listdir(path))

    return [ex_name for ex_name in all_names if exists(path, ex_name)]
