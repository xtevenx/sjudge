import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

import platform
import pytest

from command import _exists
from command import get_command

WINDOWS = "Windows"


def test___exists():
    assert _exists("python" if platform.system() == WINDOWS else "python3") is True
    assert _exists("testtesttest") is False


def test__get_command():
    assert get_command("main") == "./main"
    assert get_command("main.exe") == "./main.exe"

    c = "python main.pyc" if platform.system() == WINDOWS else "python3 main.pyc"
    assert get_command("main.pyc") == c

    c = "python main.py" if platform.system() == WINDOWS else "python3 main.py"
    assert get_command("main.py") == c

    # test for `get_command` failure.
    import command
    command.LANGUAGES[frozenset({"test"})] = ("testtesttest",) * 2

    with pytest.raises(AssertionError):
        assert get_command("main.test")
