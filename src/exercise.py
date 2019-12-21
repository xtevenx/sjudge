import os
import typing

REQUIRED_COMPONENTS = [
    "json",  # problems & solutions
    "txt",  # problem description
]


def get_exercises_list(exercises_directory: str) -> typing.List[str]:
    found_lessons: typing.List[str] = []
    failed_lessons: typing.List[str] = []

    all_files: typing.Iterable[str] = os.listdir(exercises_directory)
    all_files = (
        f.split(".")[0] for f in all_files
        if (f.split(".")[0] not in found_lessons
            and f.split(".")[0] not in failed_lessons)
    )

    for exercise_name in all_files:
        for file_ext in REQUIRED_COMPONENTS:
            path: str = os.path.join(exercises_directory, f"{exercise_name}.{file_ext}")
            if not os.path.isfile(path):
                break
        else:
            found_lessons.append(exercise_name)
            continue
        failed_lessons.append(exercise_name)

    return sorted(found_lessons)
