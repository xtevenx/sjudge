import shlex
import subprocess
import sys
import time
import typing

from judges import float_judge
from judges import identical_judge
from judges import default_judge
import truncate

TEST_IO_TYPE: typing.Type = typing.List[str]

TESTCASE_TYPE: typing.Type = typing.List[
    typing.Tuple[TEST_IO_TYPE, TEST_IO_TYPE]
]

ANSWER_CORRECT = "Answer Correct"
RUNTIME_ERROR = "Runtime Error"
TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
WRONG_ANSWER = "Wrong Answer"

JUDGE_TYPE: typing.Type = typing.Callable[
    [typing.List[str], typing.List[str]], bool
]

ANY_JUDGE: typing.Type = typing.Union[str, JUDGE_TYPE]

JUDGES: typing.Dict[str, JUDGE_TYPE] = {
    "float": float_judge.float_judge,
    "identical": identical_judge.identical_judge,
    "default": default_judge.default_judge
}

TRUNCATOR_TYPE = typing.Callable[[typing.List[str]], typing.List[str]]

DEFAULT_TRUNCATOR: TRUNCATOR_TYPE = lambda s: truncate.truncate(s, 80, 3)


class TestcaseResult:
    def __init__(self, given_input: TEST_IO_TYPE, given_output: TEST_IO_TYPE,
                 received_output: TEST_IO_TYPE, error_message: TEST_IO_TYPE,
                 exitcode: int = False, time_for_test: float = 0,
                 time_limit_exceeded: bool = False,
                 judge_function: ANY_JUDGE = "default"):
        self.given_input: TEST_IO_TYPE = given_input
        self.given_output: TEST_IO_TYPE = given_output
        self.received_output: TEST_IO_TYPE = received_output
        self.error_message: TEST_IO_TYPE = error_message
        self.exitcode: int = exitcode
        self.time_for_test: float = time_for_test
        self.time_limit_exceeded: bool = time_limit_exceeded

        if type(judge_function) == str:
            judge_function = JUDGES[judge_function]
        self.judge_function: JUDGE_TYPE = judge_function

        self.verdict: str = self._get_verdict()
        self.passed: bool = self.verdict == ANSWER_CORRECT

    def _get_verdict(self) -> str:
        if self.time_limit_exceeded:
            return TIME_LIMIT_EXCEEDED
        elif self.exitcode:
            return RUNTIME_ERROR
        else:
            judge_result: bool = self.judge_function(
                self.received_output, self.given_output
            )

            return ANSWER_CORRECT if judge_result else WRONG_ANSWER


class JudgeResult:
    def __init__(self) -> None:
        self.testcases: typing.List[TestcaseResult] = []

        self.passed_testcases: int = 0
        self.total_testcases: int = 0
        self.maximum_time: float = 0.0
        self.verdict: str = ANSWER_CORRECT

    def __add__(self, other: TestcaseResult) -> "JudgeResult":
        self.add_result(other)
        return self

    def __getitem__(self, item: int) -> TestcaseResult:
        return self.testcases[item]

    def __iter__(self) -> iter:
        return iter(self.testcases)

    def add_result(self, tc: TestcaseResult) -> None:
        self.testcases.append(tc)

        self.passed_testcases += tc.passed
        self.total_testcases += 1
        self.maximum_time = max(self.maximum_time, tc.time_for_test)

        if self.verdict == ANSWER_CORRECT and tc.verdict != ANSWER_CORRECT:
            self.verdict = tc.verdict


def judge_file(file_command: str, testcases: TESTCASE_TYPE,
               time_limit: float = 1.0,
               truncator: TRUNCATOR_TYPE = DEFAULT_TRUNCATOR) -> JudgeResult:
    result_tracker = JudgeResult()

    for test_number, (test_input, test_output) in enumerate(testcases):
        start_time = time.time()

        try:
            process_return = subprocess.run(
                shlex.split(file_command),
                input=_encode_io(test_input),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=time_limit,
                universal_newlines=True
            )

            process_output = _decode_io(process_return.stdout)
            process_errors = _decode_io(process_return.stderr)
            process_exitcode = process_return.returncode

            result_tracker += TestcaseResult(
                test_input, test_output, process_output, process_errors,
                process_exitcode, time_for_test=1000 * (time.time() - start_time)
            )

        except subprocess.TimeoutExpired as ex:
            result_tracker += TestcaseResult(
                test_input, test_output, [""], [""], 1,
                time_for_test=1000 * ex.timeout,
                time_limit_exceeded=True
            )

        finally:
            elapsed_time = 1000 * (time.time() - start_time)
            elapsed_time = min(1000 * time_limit, elapsed_time)

            this_result = result_tracker[-1]
            _display("Case #{} → {}  [{} ms]".format(
                test_number + 1,
                this_result.verdict,
                round(elapsed_time)
            ))

            if this_result.verdict == RUNTIME_ERROR:
                _display("\n".join(
                    f"  - {s}" for s in truncator(this_result.error_message)
                ))
                _display("  - Process finished with exit code {}".format(
                    this_result.exitcode
                ))

            elif this_result.verdict == WRONG_ANSWER:
                _display("  - Expected output:")
                _display("\n".join(
                    f"  - {s}" for s in truncator(this_result.given_output)
                ))

                _display("  - Received output:")
                _display("\n".join(
                    f"  - {s}" for s in truncator(this_result.received_output)
                ))

    details: str = (
        f"{result_tracker.maximum_time:.0f} ms"
        if result_tracker.verdict == ANSWER_CORRECT else
        result_tracker.verdict
    )
    _display("Final score: {}/{}  [{}]".format(
        result_tracker.passed_testcases,
        result_tracker.total_testcases,
        details
    ))
    return result_tracker


def _encode_io(given_io: TEST_IO_TYPE) -> str:
    return "".join(
        f"{input_line}\n" for input_line in given_io
    )


def _decode_io(process_io: str) -> TEST_IO_TYPE:
    return [
        s.strip("".join(['\r', '\n']))
        for s in process_io.strip().split("\n")
    ]


def _display(s: str) -> None:
    sys.stdout.write(f"{s}\n")
    sys.stdout.flush()
