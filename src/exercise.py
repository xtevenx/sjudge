import json
import os
import typing

SPEC_TYPE: typing.Type = typing.Dict[typing.AnyStr, typing.Any]

REQUIRED_COMPONENTS: typing.List[str] = [
    "json",  # problem specifications
    "txt",  # problem description
]

SPEC_FORMATTING: typing.Dict[str, str] = {
    "problem": "{key}: {value}\n",
    "time_limit": "{key}: {value} s",
    "memory_limit": "{key}: {value} MiB",
}


def get_exercises_list(exercises_directory: str) -> typing.List[str]:
    assert os.path.isdir(exercises_directory), \
        f"The exercises location `{exercises_directory}` is not a directory."

    found_lessons: typing.List[str] = []
    failed_lessons: typing.List[str] = []

    all_files: typing.Iterable[str] = (
        f.split(".")[0] for f in os.listdir(exercises_directory)
        if f.split(".")[0] not in found_lessons and f.split(".")[0] not in failed_lessons
    )

    for exercise_name in all_files:
        for file_ext in REQUIRED_COMPONENTS:
            path = os.path.join(exercises_directory, f"{exercise_name}.{file_ext}")
            if not os.path.isfile(path):
                break
        else:
            found_lessons.append(exercise_name)
            continue
        failed_lessons.append(exercise_name)

    return sorted(found_lessons)


def get_exercise_description(exercises_directory: str, exercise_name: str) -> str:
    description = ""

    spec_path = os.path.join(exercises_directory, f"{exercise_name}.json")
    specs: SPEC_TYPE = json.load(open(spec_path, "r"))
    for key, value in specs.items():
        if key == "testcases":
            continue
        formatted_key = key.replace("_", " ").capitalize()

        try:
            description += SPEC_FORMATTING[key].format(
                key=formatted_key, value=value
            ) + "\n"
        except KeyError:
            description += f"{formatted_key}: {value}\n"

    description += "\n"

    file_path = os.path.join(exercises_directory, f"{exercise_name}.txt")
    file_handle = open(file_path, "r")
    description += file_handle.read()
    file_handle.close()

    return description
