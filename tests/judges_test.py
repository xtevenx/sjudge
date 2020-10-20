import _template

from judges.default_judge import default_judge
from judges.float_judge import float_judge
from judges.identical_judge import identical_judge


def test__default_judge__indentical():
    assert default_judge([], [])
    assert default_judge(["abc"], ["abc"])
    assert default_judge(["a", "b", "c"], ["a", "b", "c"])
    assert default_judge(["abc", "def"], ["abc", "def"])


def test__default_judge__strip():
    assert default_judge([" abc ", "  def   "], ["abc", "def"])
    assert default_judge(["abc", "def"], ["   abc  ", " def "])
    assert default_judge([" abc ", "  def   "], ["   abc  ", " def "])


def test__default_judge__bad_lines():
    assert not default_judge([], ["abc"])
    assert not default_judge(["abc"], [])
    assert not default_judge(["abc"], ["def"])


def test__default_judge__bad_chars():
    assert not default_judge(["a", "b", "c"], ["a", "b"])
    assert not default_judge(["a", "b"], ["a", "b", "c"])
    assert not default_judge(["a", "b", "c"], ["a", "b", "d"])
    assert not default_judge(["a", "b", "cd"], ["a", "b", "c"])


def test__float_judge__identical():
    assert float_judge([], [])
    assert float_judge(["123"], ["123"])
    assert float_judge(["1", "2", "3"], ["1", "2", "3"])
    assert float_judge(["123", "456"], ["123", "456"])


def test__float_judge__strip():
    assert float_judge([" 123 ", "  456   "], ["123", "456"])
    assert float_judge(["123", "456"], ["   123  ", " 456 "])
    assert float_judge([" 123 ", "  456   "], ["   123  ", " 456 "])


def test__float_judge__bad_lines():
    assert not float_judge([], ["123"])
    assert not float_judge(["123"], [])
    assert not float_judge(["123"], ["456"])


def test__float_judge__bad_chars():
    assert not float_judge(["1", "2", "3"], ["1", "2"])
    assert not float_judge(["1", "2"], ["1", "2", "3"])
    assert not float_judge(["1", "2", "3"], ["1", "2", "4"])
    assert not float_judge(["1", "2", "34"], ["1", "2", "3"])


def test__float_judge__rounding():
    assert float_judge(["123.04"], ["123"], precision=1)
    assert float_judge(["1.23", "2.72", "3.14159265358"], ["1.234", "2.71848", "3.14"], precision=2)
    assert not float_judge(["123.04"], ["123"], precision=2)
    assert not float_judge(["1.23", "2.72", "3.14159265358"], ["1.234", "2.71848", "3.14"], precision=3)


def test__float_judge__bad_structure():
    assert float_judge(["1.23 2.72 3.14159265358"], ["1.234 2.71848 3.14"], precision=2)
    assert not float_judge(["1.23 2.72 3.14159265358"], ["1.234 2.71848 3.14"], precision=3)
    assert not float_judge(["1.23 2.72 3.14159265358"], ["1.234 2.71848"], precision=2)
    assert not float_judge(["1.23 2.72"], ["1.234 2.71848 3.14"], precision=3)


def test__float_judge__not_float():
    assert not float_judge(["1.test 2.72 3.14159265358"], ["1.234 2.71848 3.14"], precision=2)
    assert not float_judge(["1.23 test test_again"], ["1.234 2.71848 3.14"], precision=3)


def test__identical_judge():
    assert identical_judge([], [])
    assert identical_judge(["abc"], ["abc"])
    assert identical_judge(["a", "b", "c"], ["a", "b", "c"])
    assert identical_judge(["abc", "def"], ["abc", "def"])

    assert not identical_judge([" abc ", "  def   "], ["abc", "def"])
    assert not identical_judge(["abc", "def"], ["   abc  ", " def "])
    assert not identical_judge([" abc ", "  def   "], ["   abc  ", " def "])

    assert not identical_judge([], ["abc"])
    assert not identical_judge(["abc"], [])
    assert not identical_judge(["abc"], ["def"])

    assert not identical_judge(["a", "b", "c"], ["a", "b"])
    assert not identical_judge(["a", "b"], ["a", "b", "c"])
    assert not identical_judge(["a", "b", "c"], ["a", "b", "d"])
    assert not identical_judge(["a", "b", "cd"], ["a", "b", "c"])
