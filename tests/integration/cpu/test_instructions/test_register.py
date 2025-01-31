import pytest

from src.cpu.instructions.register import Register


@pytest.fixture
def register(bus):
    return Register(bus.cpu)


def test_tax(bus, register, time_instruction) -> None:
    """Tests the tax (Transfer Accumulator to X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x42  # Accumulator value

    # Execute instruction
    register.tax()

    # Expected results
    expected_x = bus.cpu.a
    expected_zero = expected_x == 0
    expected_negative = (expected_x & 0x80) != 0

    # Verify results
    assert bus.cpu.x == expected_x, (
        f"X should be {hex(expected_x)}, but got {hex(bus.cpu.x)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "TAX should take 2 cycles"


def test_tay(bus, register, time_instruction) -> None:
    """Tests the tay (Transfer Accumulator to Y) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x99  # Accumulator value

    # Execute instruction
    register.tay()

    # Expected results
    expected_y = bus.cpu.a
    expected_zero = expected_y == 0
    expected_negative = (expected_y & 0x80) != 0

    # Verify results
    assert bus.cpu.y == expected_y, (
        f"Y should be {hex(expected_y)}, but got {hex(bus.cpu.y)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "TAY should take 2 cycles"


def test_txa(bus, register, time_instruction) -> None:
    """Tests the txa (Transfer X to Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x55  # X register value

    # Execute instruction
    register.txa()

    # Verify results
    assert bus.cpu.a == bus.cpu.x, (
        f"A should be {hex(bus.cpu.x)}, but got {hex(bus.cpu.a)}"
    )
    assert bus.cpu.cycles == 2, "TXA should take 2 cycles"


def test_tya(bus, register, time_instruction) -> None:
    """Tests the tya (Transfer Y to Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0xAA  # Y register value

    # Execute instruction
    register.tya()

    # Verify results
    assert bus.cpu.a == bus.cpu.y, (
        f"A should be {hex(bus.cpu.y)}, but got {hex(bus.cpu.a)}"
    )
    assert bus.cpu.cycles == 2, "TYA should take 2 cycles"


def test_dex(bus, register, time_instruction) -> None:
    """Tests the dex (Decrement X Register) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x01  # X register value

    # Execute instruction
    register.dex()

    # Expected results
    expected_x = (0x01 - 1) & 0xFF  # Should be 0x00
    expected_zero = expected_x == 0
    expected_negative = (expected_x & 0x80) != 0

    # Verify results
    assert bus.cpu.x == expected_x, (
        f"X should be {hex(expected_x)}, but got {hex(bus.cpu.x)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "DEX should take 2 cycles"


def test_dey(bus, register, time_instruction) -> None:
    """Tests the dey (Decrement Y Register) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x80  # Y register value

    # Execute instruction
    register.dey()

    # Expected results
    expected_y = (0x80 - 1) & 0xFF  # Should be 0x7F
    expected_zero = expected_y == 0
    expected_negative = (expected_y & 0x80) != 0

    # Verify results
    assert bus.cpu.y == expected_y, (
        f"Y should be {hex(expected_y)}, but got {hex(bus.cpu.y)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "DEY should take 2 cycles"


def test_inx(bus, register, time_instruction) -> None:
    """Tests the inx (Increment X Register) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0xFF  # X register value

    # Execute instruction
    register.inx()

    # Expected results
    expected_x = (0xFF + 1) & 0xFF  # Should wrap around to 0x00
    expected_zero = expected_x == 0
    expected_negative = (expected_x & 0x80) != 0

    # Verify results
    assert bus.cpu.x == expected_x, (
        f"X should be {hex(expected_x)}, but got {hex(bus.cpu.x)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "INX should take 2 cycles"


def test_iny(bus, register, time_instruction) -> None:
    """Tests the iny (Increment Y Register) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x7F  # Y register value

    # Execute instruction
    register.iny()

    # Expected results
    expected_y = (0x7F + 1) & 0xFF  # Should be 0x80
    # Verify results
    assert bus.cpu.y == expected_y, (
        f"Y should be {hex(expected_y)}, but got {hex(bus.cpu.y)}"
    )
    assert bus.cpu.cycles == 2, "INY should take 2 cycles"
