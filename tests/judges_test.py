from tests import _template

import src


def test__default_judge__indentical():
    assert src.judges.default_judge([], [])
    assert src.judges.default_judge(["abc"], ["abc"])
    assert src.judges.default_judge(["a", "b", "c"], ["a", "b", "c"])
    assert src.judges.default_judge(["abc", "def"], ["abc", "def"])


def test__default_judge__strip():
    assert src.judges.default_judge([" abc ", "  def   "], ["abc", "def"])
    assert src.judges.default_judge(["abc", "def"], ["   abc  ", " def "])
    assert src.judges.default_judge([" abc ", "  def   "], ["   abc  ", " def "])


def test__default_judge__bad_lines():
    assert not src.judges.default_judge([], ["abc"])
    assert not src.judges.default_judge(["abc"], [])
    assert not src.judges.default_judge(["abc"], ["def"])


def test__default_judge__bad_chars():
    assert not src.judges.default_judge(["a", "b", "c"], ["a", "b"])
    assert not src.judges.default_judge(["a", "b"], ["a", "b", "c"])
    assert not src.judges.default_judge(["a", "b", "c"], ["a", "b", "d"])
    assert not src.judges.default_judge(["a", "b", "cd"], ["a", "b", "c"])


def test__float_judge__identical():
    assert src.judges.float_judge([], [])
    assert src.judges.float_judge(["123"], ["123"])
    assert src.judges.float_judge(["1", "2", "3"], ["1", "2", "3"])
    assert src.judges.float_judge(["123", "456"], ["123", "456"])


def test__float_judge__strip():
    assert src.judges.float_judge([" 123 ", "  456   "], ["123", "456"])
    assert src.judges.float_judge(["123", "456"], ["   123  ", " 456 "])
    assert src.judges.float_judge([" 123 ", "  456   "], ["   123  ", " 456 "])


def test__float_judge__bad_lines():
    assert not src.judges.float_judge([], ["123"])
    assert not src.judges.float_judge(["123"], [])
    assert not src.judges.float_judge(["123"], ["456"])


def test__float_judge__bad_chars():
    assert not src.judges.float_judge(["1", "2", "3"], ["1", "2"])
    assert not src.judges.float_judge(["1", "2"], ["1", "2", "3"])
    assert not src.judges.float_judge(["1", "2", "3"], ["1", "2", "4"])
    assert not src.judges.float_judge(["1", "2", "34"], ["1", "2", "3"])


def test__float_judge__rounding():
    assert src.judges.float_judge(["123.04"], ["123"], precision=1)
    assert src.judges.float_judge(["1.23", "2.72", "3.14159265358"], ["1.234", "2.71848", "3.14"], precision=2)
    assert not src.judges.float_judge(["123.04"], ["123"], precision=2)
    assert not src.judges.float_judge(["1.23", "2.72", "3.14159265358"], ["1.234", "2.71848", "3.14"], precision=3)


def test__float_judge__bad_structure():
    assert src.judges.float_judge(["1.23 2.72 3.14159265358"], ["1.234 2.71848 3.14"], precision=2)
    assert not src.judges.float_judge(["1.23 2.72 3.14159265358"], ["1.234 2.71848 3.14"], precision=3)
    assert not src.judges.float_judge(["1.23 2.72 3.14159265358"], ["1.234 2.71848"], precision=2)
    assert not src.judges.float_judge(["1.23 2.72"], ["1.234 2.71848 3.14"], precision=3)


def test__float_judge__not_float():
    assert not src.judges.float_judge(["1.test 2.72 3.14159265358"], ["1.234 2.71848 3.14"], precision=2)
    assert not src.judges.float_judge(["1.23 test test_again"], ["1.234 2.71848 3.14"], precision=3)


def test__identical_judge():
    assert src.judges.identical_judge([], [])
    assert src.judges.identical_judge(["abc"], ["abc"])
    assert src.judges.identical_judge(["a", "b", "c"], ["a", "b", "c"])
    assert src.judges.identical_judge(["abc", "def"], ["abc", "def"])

    assert not src.judges.identical_judge([" abc ", "  def   "], ["abc", "def"])
    assert not src.judges.identical_judge(["abc", "def"], ["   abc  ", " def "])
    assert not src.judges.identical_judge([" abc ", "  def   "], ["   abc  ", " def "])

    assert not src.judges.identical_judge([], ["abc"])
    assert not src.judges.identical_judge(["abc"], [])
    assert not src.judges.identical_judge(["abc"], ["def"])

    assert not src.judges.identical_judge(["a", "b", "c"], ["a", "b"])
    assert not src.judges.identical_judge(["a", "b"], ["a", "b", "c"])
    assert not src.judges.identical_judge(["a", "b", "c"], ["a", "b", "d"])
    assert not src.judges.identical_judge(["a", "b", "cd"], ["a", "b", "c"])
