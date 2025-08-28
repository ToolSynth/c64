import pytest

from src.bus.bus import Bus
from src.bus.memory.rom import ROM


@pytest.fixture
def bus(monkeypatch):
    """Inicjalizuje magistralę w trybie testowym z zaślepkami ROM."""

    def fake_post_init(self):
        self.data = bytes([i % 256 for i in range(self.size)])

    monkeypatch.setattr(ROM, "__post_init__", fake_post_init, raising=False)
    b = Bus()
    yield b
    b.ram.close()
    b.color_ram.close()
