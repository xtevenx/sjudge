from tests import _template
import pytest

import shlex
import src

MEBIBYTE = 1024 * 1024
ml, tl = (64 * MEBIBYTE, 6)


def test__run__ac():
    a = shlex.split(src.command.get_command("tests/solutions/ac_tester.py"))
    c = src.run.run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode == 0
    assert c.stdout == ""
    assert c.stderr == ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded


def test__run__mle():
    a = shlex.split(src.command.get_command("tests/solutions/mle_tester.py"))
    c = src.run.run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode != 0
    assert c.stdout == ""
    assert c.stderr == ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage > ml
    assert c.memory_exceeded


def test__run__rte():
    a = shlex.split(src.command.get_command("tests/solutions/rte_tester.py"))
    c = src.run.run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode != 0
    assert c.stdout == ""
    assert c.stderr != ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded


def test__run__tle():
    a = shlex.split(src.command.get_command("tests/solutions/tle_tester.py"))
    c = src.run.run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode != 0
    assert c.stdout == ""
    assert c.stderr == ""
    assert c.time_usage > tl
    assert c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded


def test__run__wa():
    a = shlex.split(src.command.get_command("tests/solutions/wa_tester.py"))
    c = src.run.run(a, "", memory_limit=ml, time_limit=tl)
    assert c.args == a
    assert c.returncode == 0
    assert c.stdout != ""
    assert c.stderr == ""
    assert c.time_usage <= tl
    assert not c.time_exceeded
    assert c.memory_usage <= ml
    assert not c.memory_exceeded


def test__run__no_exist():
    with pytest.raises(AssertionError):
        src.run.run(["hopefullynothingiscalledthis"], "", memory_limit=ml, time_limit=tl)
