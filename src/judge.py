"""
This module manages the judging of a program. The normal usage is with
the `judge()` and `judge_one()` functions.
"""

import shlex
import typing

import display
from judges import float_judge
from judges import identical_judge
from judges import default_judge
import run
import truncate

# The "input/output format" for the testing data is a list of strings.
# Each string in the list represents a line of characters that is to be
# passed to the tested program.
IO_TYPE: typing.Type = typing.List[str]

# A test case is represented by two IO_TYPE objects. The input and its
# reference output.
TESTCASE_TYPE: typing.Type = typing.Tuple[IO_TYPE, IO_TYPE]

# A 'judge' is a function which takes in two IO_TYPE objects (the
# program's output and the reference output) and returns `True` if the
# program's output is deemed correct.
JUDGE_TYPE: typing.Type = typing.Callable[[IO_TYPE, IO_TYPE], bool]

# ANY_JUDGE represents anything that could be a judge: either a
# JUDGE_TYPE function or a string, the name of a judge.
ANY_JUDGE: typing.Type = typing.Union[str, JUDGE_TYPE]

# A 'truncator' is a function that takes in an IO_TYPE object and
# returns a truncated IO_TYPE object.
TRUNCATOR_TYPE: typing.Type = typing.Callable[[IO_TYPE], IO_TYPE]

# define judging verdicts
ANSWER_CORRECT: str = "Answer Correct"
RUNTIME_ERROR: str = "Runtime Error"
TIME_LIMIT_EXCEEDED: str = "Time Limit Exceeded"
MEM_LIMIT_EXCEEDED: str = "Memory Limit Exceeded"
WRONG_ANSWER: str = "Wrong Answer"

# define judging functions
JUDGES: typing.Dict[str, JUDGE_TYPE] = {
    "float": float_judge.float_judge,
    "identical": identical_judge.identical_judge,
    "default": default_judge.default_judge
}

# define I/O truncator
DEFAULT_TRUNCATOR: TRUNCATOR_TYPE = lambda s: truncate.truncate(s, 200, 4)

# define other utilities
MEBIBYTE: int = 1024 * 1024
MILLISECOND: int = 1000


class TestcaseResult:
    def __init__(self,
                 exercise_input: IO_TYPE, exercise_output: IO_TYPE,
                 program_stdout: IO_TYPE, program_stderr: IO_TYPE, program_exitcode: int = False,
                 program_time: float = 0, program_tle: bool = False,
                 program_memory: int = 0, program_mle: bool = False,
                 judge_func: ANY_JUDGE = "default"):
        """
        A class to keep track of a test case result.

        :param exercise_input: IO_TYPE; the input given by exercise.
        :param exercise_output: IO_TYPE; the output given by exercise.
        :param program_stdout: IO_TYPE; the test program's output.
        :param program_stderr: IO_TYPE; the test program's errors.
        :param program_exitcode: an integer; the test program's exit
            code.
        :param program_time: a float; the amount of time (in seconds)
            used by the test program.
        :param program_tle: a boolean; `True` if the test program
            exceeded the time limit.
        :param program_memory: an integer; the amount of memory (in
            bytes) used by the test program.
        :param program_mle: a boolean; `True` if the test program
            exceeded the memory limit.
        :param judge_func: ANY_JUDGE; a judging function or a string,
            the name of a judging function.
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

        if isinstance(judge_func, str):
            judge_func = JUDGES[judge_func]
        self.judge_func: JUDGE_TYPE = judge_func

        self.verdict: str = self._get_verdict()
        self.passed: bool = self.verdict == ANSWER_CORRECT

    def _get_verdict(self) -> str:
        """
        Get the verdict of this test.

        :return: a string; the judging verdict
        """

        if self.program_tle:
            return TIME_LIMIT_EXCEEDED
        elif self.program_mle:
            return MEM_LIMIT_EXCEEDED
        elif self.program_exitcode:
            return RUNTIME_ERROR
        else:
            judge_result = self.judge_func(self.program_stdout, self.exercise_output)
            return ANSWER_CORRECT if judge_result else WRONG_ANSWER


class JudgeResult:
    def __init__(self, test_results: typing.List[TestcaseResult] = ()) -> None:
        """
        A class to keep track of an entire set of tests.

        :param test_results: a list of `TestcaseResult` instances; the
            test cases of which to keep track.
        """

        self.testcases: typing.List[TestcaseResult] = []
        for tc in test_results:
            self.add_result(tc)

        self.passed: int = 0
        self.total: int = 0

        self.maximum_time: float = 0.0
        self.maximum_memory: int = 0

        self.verdict: str = ANSWER_CORRECT

    def __add__(self, other: TestcaseResult) -> "JudgeResult":
        self.add_result(other)
        return self

    def __getitem__(self, item: int) -> TestcaseResult:
        return self.testcases[item]

    def __iter__(self) -> iter:
        return iter(self.testcases)

    def add_result(self, tc: TestcaseResult) -> None:
        """
        Add a test case to this set of tests.

        :param tc: a `TestcaseResult` instance; the test case to add.
        """

        self.testcases.append(tc)

        self.passed += tc.passed
        self.total += 1

        self.maximum_time = max(self.maximum_time, tc.program_time)
        self.maximum_memory = max(self.maximum_memory, tc.program_memory)

        if self.verdict == ANSWER_CORRECT and tc.verdict != ANSWER_CORRECT:
            self.verdict = tc.verdict


def judge_program(program_command: str, testcases: typing.List[TESTCASE_TYPE],
                  exercise: str = "???", time_limit: float = 1.0, memory_limit: int = 256,
                  judge: ANY_JUDGE = "default", truncator: TRUNCATOR_TYPE = DEFAULT_TRUNCATOR
                  ) -> JudgeResult:
    """
    Judge a program on a set of test cases.

    :param program_command: a string; the command to run the program.
    :param testcases: a list of `TESTCASE_TYPE`; the inputs and their
        respective outputs for all the test cases.
    :param exercise: a string; the name of the exercise.
    :param time_limit: a float; the time limit for the exercise (in
        seconds).
    :param memory_limit: an integer; the memory limit for the exercise
        (in mebibytes).
    :param judge: ANY_JUDGE; a judging function or a string, the name
        of a judging function, for the exercise.
    :param truncator: TRUNCATOR_TYPE; the truncation function for the
        exercise.
    :return: a `JudgeResult` instance.
    """

    display.display(f"Running tests for exercise: {exercise}")
    display.display(f"  ⮡ Time limit: {MILLISECOND * time_limit:.0f} ms")
    display.display(f"  ⮡ Memory limit: {memory_limit} MiB")
    display.display(f"  ⮡ Judge: {judge}")
    display.display()

    result_tracker = JudgeResult()

    for test_number, (test_input, test_output) in enumerate(testcases):
        this_result = judge_one(
            program_command, test_input, test_output, time_limit, memory_limit, judge
        )

        display.display("Case #{} → {}  [{:.0f} ms, {:.2f} MiB]".format(
            test_number + 1,
            this_result.verdict,
            this_result.program_time,
            this_result.program_memory / MEBIBYTE
        ))

        if this_result.verdict == RUNTIME_ERROR:
            display.display("  Error Message:")
            display.display("\n".join(f"  ⮡ {s}" for s in truncator(this_result.program_stderr)))
            display.display("  Exit code:")
            display.display("  ⮡ Process finished with exit code {}".format(this_result.program_exitcode))

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
    ))

    return result_tracker


def judge_one(program_command: str, test_input: IO_TYPE, test_output: IO_TYPE,
              time_limit: float = 1.0, memory_limit: int = 256, judge: JUDGE_TYPE = "default"
              ) -> TestcaseResult:
    """
    Judge a program on a single test case.

    :param program_command: a string; the command to run the program.
    :param test_input: IO_TYPE; the input for the test case.
    :param test_output: IO_TYPE; the output for the test case
    :param time_limit: a float; the time limit for the exercise (in
        seconds).
    :param memory_limit: an integer; the memory limit for the exercise
        (in mebibytes).
    :param judge: ANY_JUDGE; a judging function or a string, the name
        of a judging function, for the exercise.
    :return: a `TestcaseResult` instance.
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

    return TestcaseResult(
        test_input, test_output, process_output, process_errors, process_exitcode,
        program_time=MILLISECOND * process_return.time_usage,
        program_tle=process_return.time_exceeded,
        program_memory=process_return.memory_usage,
        program_mle=process_return.memory_exceeded,
        judge_func=judge
    )


def _encode_io(given_io: IO_TYPE) -> str:
    return "".join(f"{input_line}\n" for input_line in given_io)


def _decode_io(process_io: str) -> IO_TYPE:
    return [s.strip("".join(['\r', '\n'])) for s in process_io.strip().split("\n")]
