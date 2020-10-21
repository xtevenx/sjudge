import _template

import pytest

import judge
from judge import judge_program
from command import get_command

MEBIBYTE = 1024 * 1024
ml, tl, tc = (32, 6, 3)


def test__judge_program__ac():
    c = get_command("tests/solutions/ac_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.ANSWER_CORRECT
    assert r.passed == r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl


def test__judge_program__mle():
    c = get_command("tests/solutions/mle_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.MEM_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory > MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl


def test__judge_program__rte():
    c = get_command("tests/solutions/rte_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.RUNTIME_ERROR
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl


def test__judge_program__tle():
    c = get_command("tests/solutions/tle_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.TIME_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time > 1000 * tl


def test__judge_program__wa():
    c = get_command("tests/solutions/wa_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.WRONG_ANSWER
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl
