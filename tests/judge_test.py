from tests import _template
import pytest

import src

MEBIBYTE = 1024 * 1024
ml, tl, tc = (64, 6, 3)


def test__judge_program__ac():
    c = src.command.get_command("tests/solutions/ac_tester.py")
    r = src.judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == src.ANSWER_CORRECT
    assert r.passed == r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl


def test__judge_program__mle():
    c = src.command.get_command("tests/solutions/mle_tester.py")
    r = src.judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == src.MEM_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory > MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl


def test__judge_program__rte():
    c = src.command.get_command("tests/solutions/rte_tester.py")
    r = src.judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == src.RUNTIME_ERROR
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl


def test__judge_program__tle():
    c = src.command.get_command("tests/solutions/tle_tester.py")
    r = src.judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == src.TIME_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time > 1000 * tl


def test__judge_program__wa():
    c = src.command.get_command("tests/solutions/wa_tester.py")
    r = src.judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == src.WRONG_ANSWER
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl
