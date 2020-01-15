import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

import judge
from judge import judge_program
from command import get_command

MEBIBYTE = 1024 * 1024


def test__judge_program():
    ml, tl, tc = (256 * MEBIBYTE, 1000, 10)

    c = get_command("tests/solutions/ac_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], )
    assert r.verdict == judge.ANSWER_CORRECT
    assert r.passed == r.total == tc
    assert r.maximum_memory <= ml
    assert r.maximum_time <= tl

    c = get_command("tests/solutions/mle_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], )
    assert r.verdict == judge.MEM_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory > ml
    assert r.maximum_time <= tl

    c = get_command("tests/solutions/rte_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], )
    assert r.verdict == judge.RUNTIME_ERROR
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= ml
    assert r.maximum_time <= tl

    c = get_command("tests/solutions/tle_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], )
    assert r.verdict == judge.TIME_LIMIT_EXCEEDED
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= ml
    assert r.maximum_time > tl

    c = get_command("tests/solutions/wa_tester.py")
    r = judge_program(c, [([""], [""]) for _ in range(tc)], )
    assert r.verdict == judge.WRONG_ANSWER
    assert r.passed == 0
    assert r.total == tc
    assert r.maximum_memory <= ml
    assert r.maximum_time <= tl
