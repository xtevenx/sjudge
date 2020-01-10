import platform
import shlex
import subprocess
import sys

WINDOWS = "Windows"

TESTS = [
    "python3 src/main.py --list_exercises",
    "python3 src/main.py --see_description linear_algebra",

    "python3 src/main.py --exercises_location src/exercises",
    "python3 src/main.py --exercises_location src/exercises --help",
    "python3 src/main.py --exercises_location src/exercises --list_exercises",
    "python3 src/main.py --exercises_location src/exercises --see_description linear_algebra",
    "python3 src/main.py --exercises_location src/exercises --see_description _template",

    "python3 src/main.py --exercises_location src/exercises divide",
    "python3 src/main.py --exercises_location src/exercises src/solutions/divide.py",
    "python3 src/main.py --exercises_location src/exercises divide src/solutions/divide.py",
    "python3 src/main.py --exercises_location src/exercises divide src/solutions/",
    "python3 src/main.py --exercises_location src/exercises JQZ_test JQZ_test",
]

for i, s in enumerate(TESTS):
    sys.stdout.write(f"---- RUNNING TEST {i + 1} of {TESTS.__len__()} ----\n")
    sys.stdout.flush()

    if platform.system() == WINDOWS:
        s = s[:s.find("3")] + s[s.find("3") + 1:]
    result = subprocess.run(shlex.split(s))

    if result.returncode != 0:
        sys.exit(result.returncode)
