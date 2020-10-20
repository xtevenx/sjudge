import _template

from truncate import truncate


def test__no_truncate():
    assert truncate(["abc", "def"]) == ["abc", "def"]
    assert truncate(["abc", "def"], char_limit=72) == ["abc", "def"]
    assert truncate(["abc", "def"], nl_limit=3) == ["abc", "def"]
    assert truncate(["abc", "def"], char_limit=6, nl_limit=2) == ["abc", "def"]


def test__one_truncate():
    assert truncate(["abc", "def"], char_limit=4)[:-1] == ["abc", "d"]
    assert truncate(["abc", "def"], nl_limit=1)[:-1] == ["abc"]


def test__both_truncate():
    assert truncate(["abc", "def"], char_limit=6, nl_limit=1)[:-1] == ["abc"]
    assert truncate(["abc", "def"], char_limit=3, nl_limit=2)[:-1] == ["abc"]
