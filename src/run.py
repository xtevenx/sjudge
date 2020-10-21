"""
This module contains a wrapper around `subprocess.run()` that provides
various extra features enabled by `psutil`.
"""

import psutil
import subprocess
import time

from typing import List

_REALTIME_BUFFER: float = 1.0


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

    try:
        process = psutil.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
    except FileNotFoundError as err:
        msg: str = err.args[1]
        raise AssertionError(msg[:1].lower() + msg[1:])

    process.stdin.write(stdin_string)
    process.stdin.flush()

    time_usage, memory_usage = _get_data(process)

    while process.poll() is None:
        try:
            time_usage, this_memory = _get_data(process)
            memory_usage = max(memory_usage, this_memory)

            if memory_usage > memory_limit or time_usage > time_limit:
                process.kill()

            if time.time() - process.create_time() > time_limit + _REALTIME_BUFFER:
                process.kill()

        except psutil.NoSuchProcess:
            break

    return CompletedProcess(
        args,
        process.poll(),
        time_taken=time_usage,
        timed_out=time_usage > time_limit,
        max_memory=memory_usage,
        memory_exceeded=memory_usage > memory_limit,
        stdout=process.stdout.read(),
        stderr=process.stderr.read()
    )


def _get_data(p: psutil.Process):
    with p.oneshot():
        t = p.cpu_times().user + p.cpu_times().system
        m = p.memory_info().rss

    return t, m
