import time

import pytest

from src.bus.bus import Bus


@pytest.fixture
def bus():
    """
    Simple CPU stub containing minimal logic required to test jump instructions.
    """
    return Bus()


@pytest.fixture
def time_instruction():
    """
    Fixture returning a helper function to measure execution time of any instruction/function.
    It can be called multiple times to obtain a reliable measurement.
    """

    def _time_instruction(func, repeat=1, *args, **kwargs):
        """
        Runs 'func(*args, **kwargs)' 'repeat' times and returns the total time in seconds.
        Additionally returns the average time (total_time / repeat).
        """
        start = time.perf_counter()
        for _ in range(repeat):
            func(*args, **kwargs)
        end = time.perf_counter()
        total_time = end - start
        avg_time = total_time / repeat if repeat > 0 else 0
        return total_time, avg_time

    return _time_instruction
