"""
This module contains a wrapper around `subprocess.run()` that provides
various extra features enabled by `psutil`.
"""

import psutil
import subprocess
import time
import typing

_LOCALHOST_IP = "127.0.0.1"


class CompletedProcess(subprocess.CompletedProcess):
    def __init__(self, *args, time_taken: float, timed_out: bool, max_memory: int,
                 memory_exceeded: bool, **kwargs):
        """
        This class is a descendant of `subprocess.CompletedProcess`.

        :param args: arguments to pass to the parent.
        :param time_taken: a float; the time (in seconds) it took to
            run the program.
        :param timed_out: a boolean; `True` if the program exceeded the
            time limit and was killed.
        :param max_memory: an integer; the memory (in bytes) it took to
            run the program.
        :param memory_exceeded: a boolean; `True` if the program
            exceeded the memory limit and was killed memory limit and
            was killed.
        :param kwargs: keyword arguments to pass to the parent
        """

        super().__init__(*args, **kwargs)
        self.time_usage: float = time_taken
        self.time_exceeded: bool = timed_out
        self.memory_usage: int = max_memory
        self.memory_exceeded: bool = memory_exceeded


def run(args: typing.List[str], stdin_string: str, memory_limit: int, time_limit: float
        ) -> CompletedProcess:
    """
    Run command with arguments and return a `CompletedProcess`
    instance.

    This function is a wrapper around `subprocess.run()` and provides a
    simplified interface and also measures the following metrics:
      - time usage
      - memory usage

    :param args: the sequence of program arguments
    :param stdin_string: the string to pass to the subprocess from
        standard input.
    :param memory_limit: an integer; the maximum memory (in bytes)
        allowed for the program to utilize before killing it.
    :param time_limit: a float; the maximum time (in seconds) allowed
        for the program to utilize before killing it.
    :return: a `CompletedProcess` instance.
    """

    start_time = time.time()

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

    time_usage = time.time() - start_time
    memory_usage = process.memory_info().rss

    while process.poll() is None:
        try:
            time_usage = time.time() - start_time
            memory_usage = max(memory_usage, process.memory_info().rss)

            if memory_usage > memory_limit or time_usage > time_limit:
                process.kill()

            # retrieve all the connections on the machine, then filter
            # for the ones open by the current process by comparing
            # PIDs. this is required instead of simply using
            # `process.connections()` because `process.connections()`
            # requires root access on linux based operating systems.
            p_connections = (c for c in psutil.net_connections("all") if c.pid == process.pid)
            if any(map(_illegal_connection, p_connections)):
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


def _illegal_connection(c) -> bool:
    """
    Determine whether a network connection is allowed to be kept open.
    A connection is only allowed if it connects back to the local
    machine; any other connections are 'illegal'.

    :param c: one of the return of `Process.connections()`, a named
        tuple of connection attributes; the connection data from which
        to determine whether or not it is 'illegal'.
    :return: a boolean; whether the connection is allowed.
    """

    return c.raddr != () and c.raddr.ip != _LOCALHOST_IP
