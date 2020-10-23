from tests import _template
import pytest

import copy
import src

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
    assert src.exercise.exists("tests/exercises/", "test0")
    assert src.exercise.exists("tests/exercises/", "test1")
    assert src.exercise.exists("tests/exercises/", "test2")
    assert not src.exercise.exists("tests/exercises/", "test3")
    assert not src.exercise.exists("tests/exercises/", "test4")


def test__exists__no_exist():
    assert not src.exercise.exists("tests/", "test1")
    assert not src.exercise.exists("tests/", "exercises")
    assert not src.exercise.exists("tests/exercise_test.py", "test1")


def test__get_description():
    assert src.exercise.get_description("tests/exercises/", "test0") == DEFAULT_DESCRIPTION.format(e="test0")


def test__get_description__corrupt():
    with pytest.raises(AssertionError):
        src.exercise.get_description("tests/exercises/", "test1")


def test__get_description__no_exist():
    with pytest.raises(AssertionError):
        src.exercise.get_description("tests/", "test1")

    with pytest.raises(AssertionError):
        src.exercise.get_description("tests/exercise_test.py", "test1")


def test__get_specs():
    d = copy.deepcopy(DEFAULT_SPECS)
    d["exercise"] = "test0"

    assert src.exercise.get_specs("tests/exercises/", "test0") == d


def test__get_specs__corrupt():
    with pytest.raises(AssertionError):
        src.exercise.get_description("tests/exercises/", "test1")


def test__get_specs__no_exist():
    with pytest.raises(AssertionError):
        src.exercise.get_specs("tests/", "test1")

    with pytest.raises(AssertionError):
        src.exercise.get_specs("tests/exercise_test.py", "test1")


def test__list_exercises():
    assert src.exercise.list_exercises("tests/") == []
    assert sorted(src.exercise.list_exercises("tests/exercises/")) == ["test0", "test1", "test2"]


def test__list_exercises__no_exist():
    with pytest.raises(AssertionError):
        src.exercise.list_exercises("tests/exercise_test/")

    with pytest.raises(AssertionError):
        src.exercise.list_exercises("tests/exercise_test.py")
