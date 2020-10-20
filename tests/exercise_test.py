import _template

import copy
import pytest

from exercise import exists
from exercise import get_description
from exercise import get_specs
from exercise import list_exercises

DEFAULT_SPECS = {
    "exercise": None,
    "judge": "default",
    "time_limit": 1.0,
    "memory_limit": 256,
    "testcases": []
}

DEFAULT_DESCRIPTION = """Exercise: {e}
Judge: default
Time limit: 1.0 s
Memory limit: 256 MiB

{e}"""


def test__exists():
    assert exists("tests/exercises/", "test0")
    assert exists("tests/exercises/", "test1")
    assert exists("tests/exercises/", "test2")
    assert not exists("tests/exercises/", "test3")
    assert not exists("tests/exercises/", "test4")


def test__exists__no_exist():
    assert not exists("tests/", "test1")
    assert not exists("tests/", "exercises")
    assert not exists("tests/exercise_test.py", "test1")


def test__get_description():
    assert get_description("tests/exercises/", "test0") == DEFAULT_DESCRIPTION.format(e="test0")


def test__get_description__corrupt():
    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test1")


def test__get_description__no_exist():
    with pytest.raises(AssertionError):
        get_description("tests/", "test1")

    with pytest.raises(AssertionError):
        get_description("tests/exercise_test.py", "test1")


def test__get_specs():
    d = copy.deepcopy(DEFAULT_SPECS)
    d["exercise"] = "test0"

    assert get_specs("tests/exercises/", "test0") == d


def test__get_specs__corrupt():
    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test1")


def test__get_specs__no_exist():
    with pytest.raises(AssertionError):
        get_specs("tests/", "test1")

    with pytest.raises(AssertionError):
        get_specs("tests/exercise_test.py", "test1")


def test__list_exercises():
    assert list_exercises("tests/") == []
    assert sorted(list_exercises("tests/exercises/")) == ["test0", "test1", "test2"]


def test__list_exercises__no_exist():
    with pytest.raises(AssertionError):
        list_exercises("tests/exercise_test/")

    with pytest.raises(AssertionError):
        list_exercises("tests/exercise_test.py")
