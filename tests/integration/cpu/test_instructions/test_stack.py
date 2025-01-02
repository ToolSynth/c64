import pytest

from src.cpu.instructions.stack import Stack
from src.utils.log_setup import log


@pytest.fixture
def stack(bus):
    return Stack(bus.cpu)


def test_pha(bus, stack, time_instruction):
    """Tests the pha (Push Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x42  # Accumulator value
    bus.cpu.sp = 0xFD  # Initial stack pointer

    # Execute instruction
    stack.pha()

    # Expected results
    expected_sp = 0xFC  # SP should decrement
    expected_stack_value = bus.cpu.a

    # Verify results
    assert bus.cpu.sp == expected_sp, (
        f"SP should be {hex(expected_sp)}, but got {hex(bus.cpu.sp)}"
    )
    assert bus.cpu.bus.read(0x0100 + expected_sp + 1) == expected_stack_value, (
        "Stack value incorrect"
    )
    assert bus.cpu.cycles == 3, "PHA should take 3 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(stack.pha, repeat=10000)

    log.info(
        f"[test_pha] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_pla(bus, stack, time_instruction):
    """Tests the pla (Pull Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.sp = 0xFC  # Stack pointer before pull
    bus.cpu.bus.write(0x0100 + bus.cpu.sp + 1, 0x99)  # Value stored on the stack

    # Execute instruction
    stack.pla()

    # Expected results
    expected_sp = 0xFD  # SP should increment
    expected_a = 0x99  # Accumulator should have this value
    expected_zero = expected_a == 0
    expected_negative = (expected_a & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_a, (
        f"A should be {hex(expected_a)}, but got {hex(bus.cpu.a)}"
    )
    assert bus.cpu.sp == expected_sp, (
        f"SP should be {hex(expected_sp)}, but got {hex(bus.cpu.sp)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "PLA should take 4 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(stack.pla, repeat=10000)

    log.info(
        f"[test_pla] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_txs(bus, stack, time_instruction):
    """Tests the txs (Transfer X to Stack Pointer) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0xAB  # X register value

    # Execute instruction
    stack.txs()

    # Verify results
    assert bus.cpu.sp == 0xAB, f"SP should be {hex(0xAB)}, but got {hex(bus.cpu.sp)}"
    assert bus.cpu.cycles == 2, "TXS should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(stack.txs, repeat=10000)

    log.info(
        f"[test_txs] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_php(bus, stack, time_instruction):
    """Tests the php (Push Processor Status) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.sp = 0xFD  # Initial SP
    bus.cpu.status = 0b10101010  # Example status register

    # Execute instruction
    stack.php()

    # Expected results
    expected_sp = 0xFC
    expected_status = bus.cpu.status | 0x30  # PHP forces bits 4 and 5

    # Verify results
    assert bus.cpu.sp == expected_sp, (
        f"SP should be {hex(expected_sp)}, but got {hex(bus.cpu.sp)}"
    )
    assert bus.cpu.bus.read(0x0100 + expected_sp + 1) == expected_status, (
        "Status pushed incorrectly"
    )
    assert bus.cpu.cycles == 3, "PHP should take 3 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(stack.php, repeat=10000)

    log.info(
        f"[test_php] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_plp(bus, stack, time_instruction):
    """Tests the plp (Pull Processor Status) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.sp = 0xFC  # Stack pointer before pull
    bus.cpu.bus.write(0x0100 + bus.cpu.sp + 1, 0b11001100)  # Value stored on the stack

    # Execute instruction
    stack.plp()

    # Expected results
    expected_sp = 0xFD
    expected_status = (0b11001100 & 0xEF) | 0x20  # PLP forces bit 5 and clears bit 4

    # Verify results
    assert bus.cpu.sp == expected_sp, (
        f"SP should be {hex(expected_sp)}, but got {hex(bus.cpu.sp)}"
    )
    assert bus.cpu.status == expected_status, "Status register incorrect"
    assert bus.cpu.cycles == 4, "PLP should take 4 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(stack.plp, repeat=10000)

    log.info(
        f"[test_plp] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_tsx(bus, stack, time_instruction):
    """Tests the tsx (Transfer Stack Pointer to X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.sp = 0x77  # Initial stack pointer

    # Execute instruction
    stack.tsx()

    # Expected results
    expected_x = bus.cpu.sp
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
    assert bus.cpu.cycles == 2, "TSX should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(stack.tsx, repeat=10000)

    log.info(
        f"[test_tsx] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )
