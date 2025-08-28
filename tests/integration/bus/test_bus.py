import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.bus.bus import Bus


@pytest.fixture
def bus():
    return Bus()


def test_rom_read_write(bus) -> None:
    address = 0xA123
    value = 0x55
    expected = (address - 0xA000) % 256
    assert bus.read(address) == expected
    bus.write(address, value)
    assert bus.read(address) == expected
