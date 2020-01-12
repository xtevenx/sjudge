"""
This module manages the judging of a program.
"""

import shlex
import typing

import display
from judges import float_judge
from judges import identical_judge
from judges import default_judge
import test
import truncate

IO_TYPE: typing.Type = typing.List[str]
TESTCASE_TYPE: typing.Type = typing.Tuple[IO_TYPE, IO_TYPE]
JUDGE_TYPE: typing.Type = typing.Callable[[IO_TYPE, IO_TYPE], bool]
ANY_JUDGE: typing.Type = typing.Union[str, JUDGE_TYPE]
TRUNCATOR_TYPE: typing.Type = typing.Callable[[IO_TYPE], IO_TYPE]

ANSWER_CORRECT: str = "Answer Correct"
RUNTIME_ERROR: str = "Runtime Error"
TIME_LIMIT_EXCEEDED: str = "Time Limit Exceeded"
MEM_LIMIT_EXCEEDED: str = "Memory Limit Exceeded"
WRONG_ANSWER: str = "Wrong Answer"

JUDGES: typing.Dict[str, JUDGE_TYPE] = {
    "float": float_judge.float_judge,
    "identical": identical_judge.identical_judge,
    "default": default_judge.default_judge
}

DEFAULT_TRUNCATOR: TRUNCATOR_TYPE = lambda s: truncate.truncate(s, 200, 4)


class TestcaseResult:
    def __init__(self,
                 exercise_input: IO_TYPE, exercise_output: IO_TYPE,
                 program_stdout: IO_TYPE, program_stderr: IO_TYPE, program_exitcode: int = False,
                 program_time: float = 0, program_tle: bool = False,
                 program_memory: int = 0, program_mle: bool = False,
                 judge_func: ANY_JUDGE = "default"):
        """
        A class to keep track of a test case result.
        :param exercise_input: input given by exercise
        :param exercise_output: output given by exercise
        :param program_stdout: the test program's output
        :param program_stderr: the test program's errors
        :param program_exitcode: the test program's exit code
        :param program_time: the amount of time used by the test program
        :param program_tle: whether the test program ran out of time
        :param program_memory: the amount of memory used by the test program
        :param program_mle: whether the test program ran out of memory
        :param judge_func: the judging function
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

        if type(judge_func) == str:
            judge_func = JUDGES[judge_func]
        self.judge_func: JUDGE_TYPE = judge_func

        self.verdict: str = self._get_verdict()
        self.passed: bool = self.verdict == ANSWER_CORRECT

    def _get_verdict(self) -> str:
        """
        Get the result of this test based on initialization data.
        :return: the judging verdict
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
        :param test_results: test cases of which to keep track
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
        :param tc: test case to add
        :return: None
        """

        self.testcases.append(tc)

        self.passed += tc.passed
        self.total += 1

        self.maximum_time = max(self.maximum_time, tc.program_time)
        self.maximum_memory = max(self.maximum_memory, tc.program_memory)

        if self.verdict == ANSWER_CORRECT and tc.verdict != ANSWER_CORRECT:
            self.verdict = tc.verdict


def judge_file(file_command: str, testcases: typing.List[TESTCASE_TYPE],
               exercise: str = "???", time_limit: float = 1.0, memory_limit: int = 256,
               judge: JUDGE_TYPE = "default", truncator: TRUNCATOR_TYPE = DEFAULT_TRUNCATOR
               ) -> JudgeResult:
    display.display(f"Running tests for exercise: {exercise}")
    display.display(f"  ⮡ Time limit: {1000 * time_limit:.0f} ms")
    display.display(f"  ⮡ Judge: {judge}")
    display.display()

    result_tracker = JudgeResult()

    for test_number, (test_input, test_output) in enumerate(testcases):
        process_return = test.run(
            shlex.split(file_command),
            input=_encode_io(test_input),
            timeout=time_limit,
            memory_limit=1024 * 1024 * memory_limit,
        )

        process_output = _decode_io(process_return.stdout)
        process_errors = _decode_io(process_return.stderr)
        process_exitcode = process_return.returncode

        time_taken = 1000 * min(time_limit, process_return.time_taken)
        result_tracker += TestcaseResult(
            test_input, test_output, process_output, process_errors, process_exitcode,
            program_time=time_taken,
            program_tle=process_return.timed_out,
            program_memory=process_return.max_memory,
            program_mle=process_return.memory_exceeded,
            judge_func=judge
        )

        this_result = result_tracker[-1]
        display.display("Case #{} → {}  [{:.0f} ms, {:.2f} MiB]".format(
            test_number + 1,
            this_result.verdict,
            this_result.program_time,
            this_result.program_memory / 1024 / 1024
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

    details = (
        ("{:.0f} ms, {:.2f} MiB".format(
            result_tracker.maximum_time,
            result_tracker.maximum_memory / 1024 / 1024
        ))
        if result_tracker.verdict == ANSWER_CORRECT else result_tracker.verdict
    )
    display.display("Final score: {}/{}  [{}]".format(
        result_tracker.passed, result_tracker.total, details
    ))
    return result_tracker


def judge_one(file_command: str, testcase: TESTCASE_TYPE, exercise: str = "???",
              time_limit: float = 1.0, memory_limit: int = 256,
              judge: JUDGE_TYPE = "default", truncator: TRUNCATOR_TYPE = DEFAULT_TRUNCATOR
              ) -> TestcaseResult:
    """
    Judges a file on one test case
    :param file_command:
    :param testcase:
    :param exercise:
    :param time_limit:
    :param memory_limit:
    :param judge:
    :param truncator:
    :return:
    """


def _encode_io(given_io: IO_TYPE) -> str:
    return "".join(f"{input_line}\n" for input_line in given_io)


def _decode_io(process_io: str) -> IO_TYPE:
    return [s.strip("".join(['\r', '\n'])) for s in process_io.strip().split("\n")]
