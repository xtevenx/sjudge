"""
This module manages the judging of a program. The normal usage is with
the `judge()` and `judge_one()` functions.
"""

import shlex

from typing import (
    Callable, Dict, Iterable, List, Sequence, Tuple, Union
)

import display
from judges import float_judge
from judges import identical_judge
from judges import default_judge
import run
import truncate

# The "input/output" format for the testing data is a list of strings.
# Each string in the list represents a line of characters that is to be
# passed to the tested program.
IO_TYPE = List[str]

# A test case is represented by two IO_TYPE objects: the input and its
# reference output.
TESTCASE_TYPE = Tuple[IO_TYPE, IO_TYPE]

# A 'judge' is a function which takes in two IO_TYPE objects (the
# program's output and the reference output) and returns `True` if the
# program's output is deemed correct.
JUDGE_TYPE = Callable[[IO_TYPE, IO_TYPE], bool]

# ANY_JUDGE represents anything that could be a judge: either a
# JUDGE_TYPE function or a string (the name of a judge).
ANY_JUDGE = Union[JUDGE_TYPE, str]

# A 'truncator' is a function that takes in an IO_TYPE object and
# returns a truncated IO_TYPE object.
TRUNCATOR_TYPE = Callable[[IO_TYPE], IO_TYPE]

# Define the possible judging verdicts.
ANSWER_CORRECT: str = "Answer Correct"
RUNTIME_ERROR: str = "Runtime Error"
TIME_LIMIT_EXCEEDED: str = "Time Limit Exceeded"
MEM_LIMIT_EXCEEDED: str = "Memory Limit Exceeded"
WRONG_ANSWER: str = "Wrong Answer"

# Define the built-in judging functions.
JUDGES: Dict[str, JUDGE_TYPE] = {
    "float": float_judge.float_judge,
    "identical": identical_judge.identical_judge,
    "default": default_judge.default_judge
}

# Define the output truncator.
DEFAULT_TRUNCATOR: TRUNCATOR_TYPE = lambda s: truncate.truncate(s, 200, 4)

# Define the other utility constants.
MEBIBYTE: int = 1024 * 1024
MILLISECOND: float = 1000


class TestCaseResult:
    def __init__(self,
                 exercise_input: IO_TYPE, exercise_output: IO_TYPE,
                 program_stdout: IO_TYPE, program_stderr: IO_TYPE,
                 program_exitcode: int,
                 verdict: str = ANSWER_CORRECT,
                 program_time: float = 0, program_tle: bool = False,
                 program_memory: int = 0, program_mle: bool = False):
        """
        A class to keep track of a test case result.

        :param IO_TYPE exercise_input:
            The input of this particular test case.

        :param IO_TYPE exercise_output:
            The output of this particular test case.

        :param IO_TYPE program_stdout:
            The output of the program on this test case.

        :param IO_TYPE program_stderr:
            The `stderr` of the program on this test case.

        :param int program_exitcode:
            The exit code of the program.

        :param str verdict:
            The verdict of the judging; the possible values are defined
            above as constants.

        :param float program_time:
            The amount of time (in milliseconds) used by the program.

        :param bool program_tle:
            Whether the program exceeded the time limit: `True` if it
            did, otherwise `False`.

        :param int program_memory:
            The amount of memory (in bytes) used by the program.

        :param bool program_mle:
            Whether the program exceeded the memory limit: `True` if it
            did, otherwise `False`.
        """

        self.exercise_input: IO_TYPE = exercise_input
        self.exercise_output: IO_TYPE = exercise_output
        self.program_stdout: IO_TYPE = program_stdout
        self.program_stderr: IO_TYPE = program_stderr
        self.program_exitcode: int = program_exitcode
        self.program_time: float = program_time
        self.program_tle: bool = program_tle
        self.program_memory: int = program_memory
        self.program_mle: bool = program_mle

        self.verdict: str = verdict
        self.passed: bool = self.verdict == ANSWER_CORRECT


class JudgeResult:
    def __init__(self, test_results: Sequence[TestCaseResult] = ()) -> None:
        """
        A class to keep track of an entire set of test cases.
        """

        self.passed: int = 0
        self.total: int = 0

        self.maximum_time: float = 0.0
        self.maximum_memory: int = 0

        self.verdict: str = ANSWER_CORRECT

        self.testcases: List[TestCaseResult] = []
        for tc in test_results:
            self.add_result(tc)

    def __add__(self, other: TestCaseResult) -> "JudgeResult":
        self.add_result(other)
        return self

    def __getitem__(self, item: int) -> TestCaseResult:
        return self.testcases[item]

    def __iter__(self) -> Iterable[TestCaseResult]:
        return iter(self.testcases)

    def add_result(self, tc: TestCaseResult) -> None:
        """
        Add a test case to this set of tests.
        """

        self.testcases.append(tc)

        self.passed += tc.passed
        self.total += 1

        self.maximum_time = max(self.maximum_time, tc.program_time)
        self.maximum_memory = max(self.maximum_memory, tc.program_memory)

        if self.verdict == ANSWER_CORRECT and tc.verdict != ANSWER_CORRECT:
            self.verdict = tc.verdict


def judge_program(program_command: str,
                  testcases: Sequence[TESTCASE_TYPE],
                  exercise: str = "???",
                  time_limit: float = 1.0,
                  memory_limit: int = 256,
                  judge: ANY_JUDGE = "default",
                  truncator: TRUNCATOR_TYPE = DEFAULT_TRUNCATOR
                  ) -> JudgeResult:
    """
    Judge a program on a set of test cases.

    :param str program_command:
        The command to run the program.

    :param Sequence[TESTCASE_TYPE] testcases:
        A sequence of two item tuples, each representing a test case.
        The first value represents the input for the test case whereas
        the second value represents the reference output.

    :param str exercise:
        The name of the exercise.

    :param float time_limit:
        The time limit for the exercise (in seconds).

    :param int memory_limit:
        The memory limit for the exercise (in mebibytes).

    :param ANY_JUDGE judge:
        Can be one of two possibilities: a judging function of type
        `JUDGE_TYPE`, or the name of a build-in judging function.

    :param TRUNCATOR_TYPE truncator:
        The truncation function for the exercise.

    :return JudgeResult:
        ...
    """

    display.display(f"Running tests for exercise: {exercise}")
    display.display(f"  ⮡ Time limit: {MILLISECOND * time_limit:.0f} ms")
    display.display(f"  ⮡ Memory limit: {memory_limit} MiB")
    display.display(f"  ⮡ Judge: {judge}")
    display.display()

    result_tracker = JudgeResult()

    for test_number, (test_input, test_output) in enumerate(testcases):
        this_result = judge_one(
            program_command, test_input, test_output, MILLISECOND * time_limit, memory_limit, judge
        )

        display.display("Case #{} → {}  [{:.0f} ms, {:.2f} MiB]".format(
            test_number + 1,
            this_result.verdict,
            this_result.program_time,
            this_result.program_memory / MEBIBYTE
        ), v=display.RESULT_ONLY)

        if this_result.verdict == RUNTIME_ERROR:
            display.display("  Error Message:")
            display.display("\n".join(f"  ⮡ {s}" for s in truncator(this_result.program_stderr)))
            display.display("  Exit code:")
            display.display("  ⮡ Process finished with exit code {}".format(
                this_result.program_exitcode
            ))

        elif this_result.verdict == WRONG_ANSWER:
            display.display("  Expected output:")
            display.display("\n".join(f"  ⮡ {s}" for s in truncator(this_result.exercise_output)))
            display.display("  Received output:")
            display.display("\n".join(f"  ⮡ {s}" for s in truncator(this_result.program_stdout)))

        result_tracker += this_result

    if result_tracker.verdict == ANSWER_CORRECT:
        details = "{:.0f} ms, {:.2f} MiB".format(
            result_tracker.maximum_time, result_tracker.maximum_memory / MEBIBYTE
        )
    else:
        details = result_tracker.verdict

    display.display("Final score: {}/{}  [{}]".format(
        result_tracker.passed, result_tracker.total, details
    ), v=display.SUMMARY_ONLY)

    return result_tracker


def judge_one(program_command: str,
              test_input: IO_TYPE,
              test_output: IO_TYPE,
              time_limit: float = 1000,
              memory_limit: int = 256,
              judge: ANY_JUDGE = "default"
              ) -> TestCaseResult:
    """
    Judge a program on a single test case.

    :param str program_command:
        The command to run the program.

    :param IO_TYPE test_input:
        The input to test the program with.

    :param IO_TYPE test_output:
        The reference output to `test_input`.

    :param float time_limit:
        The time limit for the test case (in milliseconds).

    :param int memory_limit:
        The memory limit for the exercise (in mebibytes).

    :param ANY_JUDGE judge:
        Can be one of two possibilities: a judging function of type
        `JUDGE_TYPE`, or the name of a build-in judging function.

    :return TestCaseResult:
        ...
    """

    process_return = run.run(
        shlex.split(program_command),
        stdin_string=_encode_io(test_input),
        time_limit=time_limit / MILLISECOND,
        memory_limit=MEBIBYTE * memory_limit,
    )

    process_output = _decode_io(process_return.stdout)
    process_errors = _decode_io(process_return.stderr)
    process_exitcode = process_return.returncode

    if process_return.time_exceeded:
        judge_verdict = TIME_LIMIT_EXCEEDED
    elif process_return.memory_exceeded:
        judge_verdict = MEM_LIMIT_EXCEEDED
    elif process_exitcode:
        judge_verdict = RUNTIME_ERROR
    else:
        if isinstance(judge, str):
            judge = JUDGES[judge]

        if judge(process_output, test_output):
            judge_verdict = ANSWER_CORRECT
        else:
            judge_verdict = WRONG_ANSWER

    return TestCaseResult(
        test_input, test_output,
        process_output, process_errors, process_exitcode,
        verdict=judge_verdict,
        program_time=MILLISECOND * process_return.time_usage,
        program_tle=process_return.time_exceeded,
        program_memory=process_return.memory_usage,
        program_mle=process_return.memory_exceeded,
    )


def _encode_io(given_io: IO_TYPE) -> str:
    return "".join(f"{input_line}\n" for input_line in given_io)


def _decode_io(process_io: str) -> IO_TYPE:
    return [s.strip("".join(['\r', '\n'])) for s in process_io.strip().split("\n")]
