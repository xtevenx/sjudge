from tests import _template
import pytest

import platform
import src

WINDOWS: str = "Windows"


def test__get_command__default():
    assert src.command.get_command("main") == "./main"
    assert src.command.get_command("main.exe") == "./main.exe"


# I'm pretty sure all the test systems have Python installed.
def test__get_command__python():
    c = "python main.py" if platform.system() == WINDOWS else "python3 main.py"
    assert src.command.get_command("main.py") == c

    c = "python main.pyc" if platform.system() == WINDOWS else "python3 main.pyc"
    assert src.command.get_command("main.pyc") == c


# Test for get_command() failure on non-existent command.
def test__get_command__no_exist():
    non_existent = "hopefullynothingiscalledthis"
    src.command.LANGUAGES[frozenset({non_existent})] = (non_existent,)

    with pytest.raises(AssertionError):
        assert src.command.get_command(f"main.{non_existent}")
