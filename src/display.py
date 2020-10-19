"""
This module manages the logging/displaying of information.
"""

from typing import Dict

import judge as sjudge
import truncate

# characters to use when console doesn't support Unicode
SIMPLE_CHARACTERS: Dict[str, str] = {
    "⮡": "\\>",
    "→": "->",
    "⯇": "<",
    "⯈": ">",
}


def _truncator(s):
    return truncate.truncate(s, 200, 4)


def display(s: str = "", **kwargs) -> None:
    """
    Write `s` to standard output. Simplifies Unicode characters if they
    are unable to be displayed.
    """

    try:
        print(s, **kwargs)
    except UnicodeEncodeError:
        for old, new in SIMPLE_CHARACTERS.items():
            s = s.replace(old, new)
        print(s, **kwargs)


def d_exercise_specs(
        exercise: str,
        time_limit: float,
        memory_limit: int,
        judge: str,
        **kwargs
) -> None:
    """
    Display the specifications of an exercise.
    """

    display(f"Running tests for exercise: {exercise}")
    display(f"  ⮡ Time limit: {sjudge.MILLISECOND * time_limit:.0f} ms")
    display(f"  ⮡ Memory limit: {memory_limit} MiB")
    display(f"  ⮡ Judge: {judge}", flush=True)


def d_progress_hook(tc) -> None:
    """
    Progress hook to display the result of each test case.
    """

    display("Case #{} → {}  [{:.0f} ms, {:.2f} MiB]".format(
        tc.testcase_no + 1,
        tc.verdict,
        tc.program_time,
        tc.program_memory / sjudge.MEBIBYTE
    ))

    if tc.verdict == sjudge.RUNTIME_ERROR:
        display("  Error Message:")
        display("\n".join(f"  ⮡ {s}" for s in _truncator(tc.program_stderr)))
        display("  Exit code:")
        display("  ⮡ Process finished with exit code {}".format(
            tc.program_exitcode
        ))

    elif tc.verdict == sjudge.WRONG_ANSWER:
        display("  Expected output:")
        display("\n".join(f"  ⮡ {s}" for s in _truncator(tc.exercise_output)))
        display("  Received output:")
        display("\n".join(f"  ⮡ {s}" for s in _truncator(tc.program_stdout)))


def d_judging_summary(jr) -> None:
    if jr.verdict == sjudge.ANSWER_CORRECT:
        details = "{:.0f} ms, {:.2f} MiB".format(
            jr.maximum_time, jr.maximum_memory / sjudge.MEBIBYTE
        )
    else:
        details = jr.verdict

    display("Final score: {}/{}  [{}]".format(
        jr.passed, jr.total, details
    ))
