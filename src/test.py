import psutil
import subprocess
import time
import typing


class CompletedProcess(subprocess.CompletedProcess):
    def __init__(self, *args, max_memory: int, time_taken: float, timed_out: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_memory: int = max_memory
        self.time_taken: float = time_taken
        self.timed_out: bool = timed_out


def run(args: typing.List[str], input: str, timeout: float) -> CompletedProcess:
    process = psutil.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    start_time = time.time()
    process.stdin.write(input)
    process.stdin.flush()

    max_memory = 0
    while process.poll() is None:
        max_memory = max(max_memory, process.memory_full_info().rss)

        if time.time() - start_time > timeout:
            process.kill()
            break

    time_taken = time.time() - start_time

    return CompletedProcess(
        args,
        process.poll(),
        max_memory=max_memory,
        time_taken=time_taken,
        timed_out=time_taken > timeout,
        stdout=process.stdout.read(),
        stderr=process.stderr.read()
    )
