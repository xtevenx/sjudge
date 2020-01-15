import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

import platform
from command import get_command

WINDOWS = "Windows"


def test__get_command():
    assert get_command("main") == "./main"
    assert get_command("main.exe") == "./main.exe"

    assert get_command("main.jar") == "java -jar main.jar"

    c = "python main.pyc" if platform.system() == WINDOWS else "python3 main.pyc"
    assert get_command("main.pyc") == c

    c = "python main.py" if platform.system() == WINDOWS else "python3 main.py"
    assert get_command("main.py") == c
