import shlex
import subprocess

TEST_COMMANDS = [
    "python3 src/main.py"
]

for s in TEST_COMMANDS:
    subprocess.run(shlex.split(s))
