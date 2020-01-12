import psutil
import subprocess
import time
import typing


class CompletedProcess(subprocess.CompletedProcess):
    def __init__(self, *args, time_taken: float, timed_out: bool, max_memory: int,
                 memory_exceeded: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_taken: float = time_taken
        self.timed_out: bool = timed_out
        self.max_memory: int = max_memory
        self.memory_exceeded: bool = memory_exceeded


def run(args: typing.List[str], ex_input: str, memory_limit: int, timeout: float
        ) -> CompletedProcess:
    process = psutil.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    start_time = time.time()
    process.stdin.write(ex_input)
    process.stdin.flush()

    max_memory = 0
    while process.poll() is None:
        try:
            max_memory = max(max_memory, process.memory_info().rss)
        except psutil.NoSuchProcess:
            break

        if max_memory > memory_limit or time.time() - start_time > timeout:
            process.kill()
            break

    time_taken = time.time() - start_time

    return CompletedProcess(
        args,
        process.poll(),
        time_taken=time_taken,
        timed_out=time_taken > timeout,
        max_memory=max_memory,
        memory_exceeded=max_memory > memory_limit,
        stdout=process.stdout.read(),
        stderr=process.stderr.read()
    )
