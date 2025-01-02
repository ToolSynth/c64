import pytest

from src.cpu.instructions.flag import Flag
from src.utils.log_setup import log


@pytest.fixture
def flag(bus):
    return Flag(bus.cpu)


def test_clc(bus, flag, time_instruction):
    """Tests the clc (Clear Carry Flag) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status |= 0x01  # Set Carry flag before execution

    # Execute instruction
    flag.clc()

    # Verify results
    assert (bus.cpu.status & 0x01) == 0, "Carry flag should be cleared"
    assert bus.cpu.cycles == 2, "CLC should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(flag.clc, repeat=10000)
    log.info(f"[test_clc] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")


def test_cld(bus, flag, time_instruction):
    """Tests the cld (Clear Decimal Mode Flag) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status |= 0x08  # Set Decimal Mode flag before execution

    # Execute instruction
    flag.cld()

    # Verify results
    assert (bus.cpu.status & 0x08) == 0, "Decimal Mode flag should be cleared"
    assert bus.cpu.cycles == 2, "CLD should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(flag.cld, repeat=10000)
    log.info(f"[test_cld] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")


def test_sei(bus, flag, time_instruction):
    """Tests the sei (Set Interrupt Disable Flag) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status &= ~0x04  # Clear Interrupt flag before execution

    # Execute instruction
    flag.sei()

    # Verify results
    assert (bus.cpu.status & 0x04) != 0, "Interrupt Disable flag should be set"
    assert bus.cpu.cycles == 2, "SEI should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(flag.sei, repeat=10000)
    log.info(f"[test_sei] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")


def test_cli(bus, flag, time_instruction):
    """Tests the cli (Clear Interrupt Disable Flag) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status |= 0x04  # Set Interrupt flag before execution

    # Execute instruction
    flag.cli()

    # Verify results
    assert (bus.cpu.status & 0x04) == 0, "Interrupt Disable flag should be cleared"

    # Measure execution time
    total_time, avg_time = time_instruction(flag.cli, repeat=10000)
    log.info(f"[test_cli] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")


def test_sec(bus, flag, time_instruction):
    """Tests the sec (Set Carry Flag) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status &= ~0x01  # Clear Carry flag before execution

    # Execute instruction
    flag.sec()

    # Verify results
    assert (bus.cpu.status & 0x01) != 0, "Carry flag should be set"
    assert bus.cpu.cycles == 2, "SEC should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(flag.sec, repeat=10000)
    log.info(f"[test_sec] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")
