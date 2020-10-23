from tests import _template

import src


def test__no_truncate():
    assert src.truncate.truncate(["abc", "def"]) == ["abc", "def"]
    assert src.truncate.truncate(["abc", "def"], char_limit=72) == ["abc", "def"]
    assert src.truncate.truncate(["abc", "def"], nl_limit=3) == ["abc", "def"]
    assert src.truncate.truncate(["abc", "def"], char_limit=6, nl_limit=2) == ["abc", "def"]


def test__one_truncate():
    assert src.truncate.truncate(["abc", "def"], char_limit=4)[:-1] == ["abc", "d"]
    assert src.truncate.truncate(["abc", "def"], nl_limit=1)[:-1] == ["abc"]


def test__both_truncate():
    assert src.truncate.truncate(["abc", "def"], char_limit=6, nl_limit=1)[:-1] == ["abc"]
    assert src.truncate.truncate(["abc", "def"], char_limit=3, nl_limit=2)[:-1] == ["abc"]
