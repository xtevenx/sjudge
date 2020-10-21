"""
This module contains a wrapper around `subprocess.run()` that provides
various extra features enabled by `psutil`.
"""

import subprocess
import tempfile
import time

import psutil

from typing import List

# The actual time tracker uses CPU time instead of realtime, however,
# if the test program happens to just become dormant without using CPU,
# then it can possibly take an indefinite amount of time to be stopped.
# Because of this, there is a real time check to make sure the time
# spent isn't too absurd. The `_REALTIME_BUFFER` is the the fraction of
# the time the program is allowed to run without cpu time before it is
# forcibly killed.
#
# For example, if the buffer is 0.1 with a 1.0 second timeout, then the
# program is allowed 10% of it's runtime to be non-cpu time. This means
# that the program can run for 1.11 real time seconds without timing
# out because 1.11 - 0.1*1.11 == 0.999 and 0.999 < 1.0.
_REALTIME_BUFFER: float = 0.1


class CompletedProcess(subprocess.CompletedProcess):
    def __init__(
            self,
            *args,
            time_taken: float,
            timed_out: bool,
            max_memory: int,
            memory_exceeded: bool,
            **kwargs
    ):
        """
        This class is a descendant of `subprocess.CompletedProcess`
        with extra attributes to keep track of time taken and memory
        required.

        :param float time_taken:
            The time (in seconds) the process took to run.

        :param bool timed_out:
            `True` if the program exceeded the time limit and needed to
            be forcibly killed, otherwise `False`.

        :param int max_memory:
            The memory (in bytes) the process used when executing.

        :param bool memory_exceeded:
            `True` if the program exceeded the memory limit and needed
            to be forcibly killed, otherwise `False`.
        """

        super().__init__(*args, **kwargs)
        self.time_usage: float = time_taken
        self.time_exceeded: bool = timed_out
        self.memory_usage: int = max_memory
        self.memory_exceeded: bool = memory_exceeded


def run(
        args: List[str],
        stdin_string: str,
        memory_limit: int,
        time_limit: float
) -> CompletedProcess:
    """
    Run command with arguments and return a `CompletedProcess`
    instance.

    This function is a wrapper around `subprocess.run()` and provides a
    simplified interface and also measures the following metrics:
      - time usage
      - memory usage

    :param List[str] args:
        Arguments to pass to `psutil.Popen()` to start the process.

    :param str stdin_string:
        The string that is to be passed to the process through standard
        input.

    :param int memory_limit:
        The maximum memory (in bytes) the process is allowed to use;
        the process will be forcibly killed if it uses more than this
        amount of memory.

    :param float time_limit:
        The maximum time (in seconds) to run the process before
        forcibly killing it.

    :return CompletedProcess:
        ...
    """

    fp_out = tempfile.TemporaryFile()
    fp_err = tempfile.TemporaryFile()

    try:
        with tempfile.TemporaryFile() as fp_in:
            fp_in.write(bytes(stdin_string, encoding="utf-8"))
            fp_in.seek(0)

            process = psutil.Popen(
                args, stdin=fp_in, stdout=fp_out, stderr=fp_err, universal_newlines=True
            )

    except FileNotFoundError as err:
        fp_out.close()
        fp_err.close()

        raise AssertionError(err.args[1][:1].lower() + err.args[1][1:])

    time_usage, memory_usage = _get_data(process)

    while process.poll() is None:
        try:
            time_usage, this_memory = _get_data(process)
            memory_usage = max(memory_usage, this_memory)

            realtime_usage = time.time() - process.create_time()
            if max(time_usage, realtime_usage * (1.0 - _REALTIME_BUFFER)) > time_limit:
                time_usage = time_limit + 0.001
                break

            if memory_usage > memory_limit or time_usage > time_limit:
                break

        except psutil.NoSuchProcess:
            break

    while process.poll() is None:
        process.kill()

    fp_out.seek(0)
    stdout = str(fp_out.read(), encoding="utf-8")
    fp_out.close()

    fp_err.seek(0)
    stderr = str(fp_err.read(), encoding="utf-8")
    fp_err.close()

    return CompletedProcess(
        args,
        process.poll(),
        time_taken=time_usage,
        timed_out=time_usage > time_limit,
        max_memory=memory_usage,
        memory_exceeded=memory_usage > memory_limit,
        stdout=stdout,
        stderr=stderr
    )


def _get_data(p: psutil.Process):
    with p.oneshot():
        t = p.cpu_times().user + p.cpu_times().system
        m = p.memory_info().rss

    return t, m
