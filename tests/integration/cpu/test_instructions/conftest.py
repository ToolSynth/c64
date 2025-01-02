import time

import pytest

from src.bus.bus import Bus


@pytest.fixture()
def bus():
    """
    Prosta atrapa CPU, zawiera minimalną logikę potrzebną do testowania
    instrukcji skoku.
    """
    return Bus()


@pytest.fixture
def time_instruction():
    """
    Fixture zwraca funkcję pomocniczą do pomiaru czasu wykonania dowolnej instrukcji/funkcji.
    Możemy ją wywołać wielokrotnie, aby uzyskać miarodajny pomiar.
    """

    def _time_instruction(func, repeat=1, *args, **kwargs):
        """
        Uruchamia 'func(*args, **kwargs)' 'repeat' razy i zwraca łączny czas w sekundach.
        Dodatkowo zwraca średni czas (czas_całkowity / repeat).
        """
        start = time.perf_counter()
        for _ in range(repeat):
            func(*args, **kwargs)
        end = time.perf_counter()
        total_time = end - start
        avg_time = total_time / repeat if repeat > 0 else 0
        return total_time, avg_time

    return _time_instruction
