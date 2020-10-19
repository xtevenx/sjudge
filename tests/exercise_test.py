import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

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

    assert not exists("tests/", "test-1")
    assert not exists("tests/exercises/", "test-1")
    assert not exists("tests/exercise_test.py", "test-1")
    assert not exists("tests/", "exercises")


def test__get_description():
    assert get_description("tests/exercises/", "test0") == DEFAULT_DESCRIPTION.format(e="test0")

    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test1")

    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test2")

    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test3")

    with pytest.raises(AssertionError):
        get_description("tests/", "test-1")

    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test-1")

    with pytest.raises(AssertionError):
        get_description("tests/exercise_test.py", "test-1")

    with pytest.raises(AssertionError):
        get_description("tests/", "exercises")


def test__get_specs():
    d = copy.deepcopy(DEFAULT_SPECS)
    d["exercise"] = "test0"
    assert get_specs("tests/exercises/", "test0") == d

    with pytest.raises(AssertionError):
        get_description("tests/exercises/", "test1")

    with pytest.raises(AssertionError):
        get_specs("tests/exercises/", "test2")

    with pytest.raises(AssertionError):
        get_specs("tests/exercises/", "test3")

    with pytest.raises(AssertionError):
        get_specs("tests/", "test-1")

    with pytest.raises(AssertionError):
        get_specs("tests/exercises/", "test-1")

    with pytest.raises(AssertionError):
        get_specs("tests/exercise_test.py", "test-1")

    with pytest.raises(AssertionError):
        get_specs("tests/", "exercises")


def test__list_exercises():
    assert list_exercises("tests/") == []
    assert sorted(list_exercises("tests/exercises/")) == ["test0", "test1"]

    with pytest.raises(AssertionError):
        list_exercises("tests/exercise_test.py")
