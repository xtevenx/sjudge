import shlex
import subprocess
import sys

TEST_COMMANDS = [
    "python3 src/main.py"
]

for s in TEST_COMMANDS:
    result = subprocess.run(shlex.split(s))
    if result.returncode != 0:
        sys.exit(result.returncode)
