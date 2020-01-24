import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

import pytest
import shlex

from run import run
from command import get_command

MEBIBYTE = 1024 * 1024


def test__run():
    ml, tl = (64 * MEBIBYTE, 6)

    a = shlex.split(get_command("tests/solutions/ac_tester.py"))
    c = run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode == 0
    assert c.stdout == ""
    assert c.stderr == ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded

    a = shlex.split(get_command("tests/solutions/mle_tester.py"))
    c = run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode != 0
    assert c.stdout == ""
    assert c.stderr == ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage > ml
    assert c.memory_exceeded

    a = shlex.split(get_command("tests/solutions/rte_tester.py"))
    c = run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode != 0
    assert c.stdout == ""
    assert c.stderr != ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded

    a = shlex.split(get_command("tests/solutions/tle_tester.py"))
    c = run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode != 0
    assert c.stdout == ""
    assert c.stderr == ""
    assert c.time_usage > tl
    assert c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded

    a = shlex.split(get_command("tests/solutions/wa_tester.py"))
    c = run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode == 0
    assert c.stdout != ""
    assert c.stderr == ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded

    with pytest.raises(AssertionError):
        run(["testtesttest"], "", memory_limit=ml, time_limit=tl)
