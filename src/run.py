import psutil
import subprocess
import time
import typing


class CompletedProcess(subprocess.CompletedProcess):
    def __init__(self, *args, time_taken: float, timed_out: bool, max_memory: int,
                 memory_exceeded: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_usage: float = time_taken
        self.time_exceeded: bool = timed_out
        self.memory_usage: int = max_memory
        self.memory_exceeded: bool = memory_exceeded


def run(args: typing.List[str], stdin_string: str, memory_limit: int, time_limit: float
        ) -> CompletedProcess:
    start_time = time.time()

    process = psutil.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    process.stdin.write(stdin_string)
    process.stdin.flush()

    time_usage = time.time() - start_time
    memory_usage = process.memory_info().rss

    while process.poll() is None:
        try:
            time_usage = time.time() - start_time
            memory_usage = max(memory_usage, process.memory_info().rss)
        except psutil.NoSuchProcess:
            break

        if memory_usage > memory_limit or time_usage > time_limit:
            process.kill()
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
