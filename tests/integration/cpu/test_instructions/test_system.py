import pytest

from src.cpu.instructions.system import System
from src.utils.log_setup import log


@pytest.fixture
def system(bus):
    return System(bus.cpu)


def test_brk(bus, system, time_instruction):
    """Tests the brk (Break Command) instruction."""
    bus.cpu.pc = 0x2000  # Arbitrary starting address
    bus.cpu.sp = 0xFF  # Stack pointer before BRK
    bus.cpu.status = 0b00100000  # Example status with unused bit set

    # Set IRQ vector at memory location 0xFFFE/0xFFFF
    bus.write(0xFFFE, 0x34)
    bus.write(0xFFFF, 0x12)

    # Execute instruction
    system.brk()

    # Expected results
    expected_sp = bus.cpu.sp - 3  # Stack should decrease by 3
    expected_pc = 0x1234  # IRQ vector address
    expected_status = bus.cpu.status | (1 << 4)  # Break flag should be set
    expected_cycles = 7

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.sp == expected_sp, (
        f"SP should be {hex(expected_sp)}, but got {hex(bus.cpu.sp)}"
    )
    assert bus.cpu.bus.read(0x0100 + expected_sp + 2) == ((0x2001 >> 8) & 0xFF), (
        "Incorrect high byte of PC pushed"
    )
    assert bus.cpu.bus.read(0x0100 + expected_sp + 1) == (0x2001 & 0xFF), (
        "Incorrect low byte of PC pushed"
    )
    assert bus.cpu.bus.read(0x0100 + expected_sp) == expected_status, (
        "Incorrect status pushed to stack"
    )
    assert bus.cpu.cycles == expected_cycles, "BRK should take 7 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(system.brk, repeat=10000)
    log.info(f"[test_brk] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")


def test_brk_ignore_irq(bus, system, time_instruction):
    """Tests the brk (Break Command) instruction with ignore_irq=True."""
    bus.cpu.pc = 0x3000  # Arbitrary starting address

    # Execute instruction with ignore_irq=True
    system.brk(ignore_irq=True)

    # Expected results
    expected_pc = 0x3001  # PC should just advance
    expected_cycles = 0  # No additional cycles used

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, (
        "BRK with ignore_irq should not consume cycles"
    )

    # Measure execution time
    total_time, avg_time = time_instruction(
        lambda: system.brk(ignore_irq=True), repeat=10000
    )
    log.info(f"[test_brk_ignore_irq] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")


def test_nop(bus, system, time_instruction):
    """Tests the nop (No Operation) instruction."""
    bus.cpu.pc = 0x1000
    initial_cycles = bus.cpu.cycles

    # Execute instruction
    system.nop()

    # Expected results
    expected_cycles = initial_cycles + 2  # NOP should consume 2 cycles

    # Verify results
    assert bus.cpu.cycles == expected_cycles, "NOP should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(system.nop, repeat=10000)
    log.info(f"[test_nop] Total: {total_time:.6f}s, Avg: {avg_time:.9f}s")
