"""
This module manages the judging of a program. The normal usage is with
the `judge()` and `judge_one()` functions.
"""

import shlex

from typing import (
    Callable, Dict, Iterable, List, Sequence, Tuple, Union
)

from .judges import float_judge
from .judges import identical_judge
from .judges import default_judge
from . import run

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

# Define the other utility constants.
MEBIBYTE: int = 1024 * 1024
MILLISECOND: float = 1000


class TestCaseResult:
    def __init__(
            self,
            exercise_input: IO_TYPE,
            exercise_output: IO_TYPE,
            program_stdout: IO_TYPE,
            program_stderr: IO_TYPE,
            program_exitcode: int,
            verdict: str = ANSWER_CORRECT,
            program_time: float = 0,
            program_tle: bool = False,
            program_memory: int = 0,
            program_mle: bool = False
    ):
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

        # Possible attribute to say which test case this one is if it
        # belongs in a set of test cases.
        self.testcase_no: int = 0


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


def judge_program(
        program_command: str,
        testcases: Sequence[TESTCASE_TYPE],
        time_limit: float = 1.0,
        memory_limit: int = 256,
        judge: ANY_JUDGE = "default",
        progress_hook: Callable[[JudgeResult], None] = lambda tc: None,
        **kwargs
) -> JudgeResult:
    """
    Judge a program on a set of test cases.

    :param str program_command:
        The command to run the program.

    :param Sequence[TESTCASE_TYPE] testcases:
        A sequence of two item tuples, each representing a test case.
        The first value represents the input for the test case whereas
        the second value represents the reference output.

    :param float time_limit:
        The time limit for the exercise (in seconds).

    :param int memory_limit:
        The memory limit for the exercise (in mebibytes).

    :param ANY_JUDGE judge:
        Can be one of two possibilities: a judging function of type
        `JUDGE_TYPE`, or the name of a build-in judging function.

    :param Callable[[JudgeResult], None] progress_hook:
        A hook function to be called every time a test case
        completes. This function should accept an argument of
        `JudgeResult`, the result the judging up to the
        current test case.

    :param dict kwargs:
        These keyword arguments will be ignored.

    :return JudgeResult:
        ...
    """

    result_tracker = JudgeResult()

    for test_number, (test_input, test_output) in enumerate(testcases):
        result_tracker += judge_one(
            program_command,
            test_input,
            test_output,
            time_limit,
            memory_limit,
            judge,
        )

        result_tracker[-1].testcase_no = test_number
        progress_hook(result_tracker)

    return result_tracker


def judge_one(
        program_command: str,
        test_input: IO_TYPE,
        test_output: IO_TYPE,
        time_limit: float = 1.0,
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
        The time limit for the test case (in seconds).

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
        time_limit=time_limit,
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
