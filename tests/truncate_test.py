import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

from truncate import truncate


def test__truncate():
    assert truncate(["abc", "def"]) == ["abc", "def"]
    assert truncate(["abc", "def"], char_limit=72) == ["abc", "def"]
    assert truncate(["abc", "def"], nl_limit=3) == ["abc", "def"]
    assert truncate(["abc", "def"], char_limit=6, nl_limit=2) == ["abc", "def"]

    assert truncate(["abc", "def"], char_limit=4)[:-1] == ["abc", "d"]
    assert truncate(["abc", "def"], nl_limit=1)[:-1] == ["abc"]

    assert truncate(["abc", "def"], char_limit=6, nl_limit=1)[:-1] == ["abc"]
    assert truncate(["abc", "def"], char_limit=3, nl_limit=2)[:-1] == ["abc"]
