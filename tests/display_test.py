import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
source_dir = os.path.join(parent_dir, "src/")
sys.path.append(source_dir)

from display import set_verbosity


def test__set_verbosity():
    import display

    set_verbosity(display.ALL)
    assert display._VERBOSITY == display.ALL

    set_verbosity(display.RESULT_ONLY)
    assert display._VERBOSITY == display.RESULT_ONLY

    set_verbosity(display.SUMMARY_ONLY)
    assert display._VERBOSITY == display.SUMMARY_ONLY
