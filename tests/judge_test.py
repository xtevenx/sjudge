import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

import pytest

import judge
from judge import JudgeResult
from judge import judge_program
from command import get_command

MEBIBYTE = 1024 * 1024


def test__JudgeResult():
    c = get_command("tests/solutions/ac_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(10)], time_limit=2, memory_limit=256)

    r_copy = JudgeResult(r.testcases)
    for i, c in enumerate(r_copy):
        assert r[i].verdict == c.verdict
        assert r[i].program_time == c.program_time
        assert r[i].program_memory == c.program_memory


def test__judge_program():
    ml, tl, tc = (32, 6, 5)

    c = get_command("tests/solutions/ac_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.ANSWER_CORRECT
    assert r.passed == r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl

    c = get_command("tests/solutions/mle_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.MEM_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory > MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl

    c = get_command("tests/solutions/rte_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.RUNTIME_ERROR
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl

    c = get_command("tests/solutions/tle_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.TIME_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time > 1000 * tl

    c = get_command("tests/solutions/wa_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
    assert r.verdict == judge.WRONG_ANSWER
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= MEBIBYTE * ml
    assert r.maximum_time <= 1000 * tl

    with pytest.raises(AssertionError):
        c = get_command("tests/solutions/childprocess_tester.py")
        judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)

    with pytest.raises(AssertionError):
        c = get_command("tests/solutions/connections_tester.py")
        judge_program(c, [([""], [""]) for _ in range(tc)], time_limit=tl, memory_limit=ml)
