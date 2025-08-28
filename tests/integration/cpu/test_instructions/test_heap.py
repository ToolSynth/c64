import pytest

from src.cpu.instructions.heap import Heap
from src.utils.log_setup import log


@pytest.fixture
def heap(bus):
    return Heap(bus.cpu)


def test_lda_zero_page_non_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_zero_page (LDA Zero Page) instruction with a non-zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.status = 0x00  # Clear flags

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x45  # Value in memory

    # Execute instruction
    heap.lda_zero_page()

    # Expected values
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but is {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "LDA Zero Page instruction should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_zero_page, repeat=10000)

    log.info(
        f"[test_lda_zero_page_non_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_zero_page_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_zero_page (LDA Zero Page) instruction with a zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0xFF  # Initial value of A
    bus.cpu.status = 0x00  # Clear flags

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x00  # Value in memory

    # Execute instruction
    heap.lda_zero_page()

    # Expected values
    expected_value = 0x00
    expected_zero = True  # Since value is 0
    expected_negative = False  # Since bit 7 is not set

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but is {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "LDA Zero Page instruction should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_zero_page, repeat=10000)

    log.info(
        f"[test_lda_zero_page_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_zeropage_x_non_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_zeropage_x (LDA Zero Page,X) instruction with a non-zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.x = 0x05  # Offset in X register
    bus.cpu.status = 0x00  # Clear flags

    bus.ram.data[0x1000] = 0x80  # Base address in zero page
    effective_address = (0x80 + 0x05) & 0xFF  # X offset in zero page
    bus.ram.data[effective_address] = 0x45  # Value in memory

    # Execute instruction
    heap.lda_zeropage_x()

    # Expected values
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but is {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "LDA Zero Page,X instruction should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_zeropage_x, repeat=10000)

    log.info(
        f"[test_lda_zeropage_x_non_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_zeropage_x_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_zeropage_x (LDA Zero Page,X) instruction with a zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0xFF  # Initial value of A
    bus.cpu.x = 0x0A  # Offset in X register
    bus.cpu.status = 0x00  # Clear flags

    bus.ram.data[0x1000] = 0x70  # Base address in zero page
    effective_address = (0x70 + 0x0A) & 0xFF  # X offset in zero page
    bus.ram.data[effective_address] = 0x00  # Value in memory

    # Execute instruction
    heap.lda_zeropage_x()
    expected_value = 0x00
    expected_zero = True  # Since value is 0
    expected_negative = False  # Since bit 7 is not set

    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but is {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "LDA Zero Page,X instruction should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    total_time, avg_time = time_instruction(heap.lda_zeropage_x, repeat=10000)

    log.info(
        f"[test_lda_zeropage_x_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_indirect_y_no_page_cross(bus, heap, time_instruction) -> None:
    """Tests the lda_indirect_y (LDA (Indirect),Y) instruction without page crossing."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.y = 0x05  # Offset in Y register
    bus.cpu.status = 0x00  # Clear flags

    bus.ram.data[0x1000] = 0x80  # Zero-page pointer address
    bus.ram.data[0x80] = 0x34  # Low byte of target address
    bus.ram.data[0x81] = 0x12  # High byte of target address
    base_address = (0x12 << 8) | 0x34  # Construct full address
    effective_address = (base_address + 0x05) & 0xFFFF  # Account for Y
    bus.ram.data[effective_address] = 0x45  # Value in memory

    # Execute instruction
    heap.lda_indirect_y()

    # Expected values
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but is {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5, (
        "LDA (Indirect),Y instruction should take 5 cycles without page crossing"
    )
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_indirect_y, repeat=10000)

    log.info(
        f"[test_lda_indirect_y_no_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_indirect_y_page_cross(bus, heap, time_instruction) -> None:
    """Tests the lda_indirect_y (LDA (Indirect),Y) instruction with page crossing."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.y = 0xF0  # Y register offset to force page crossing
    bus.cpu.status = 0x00  # Clear flags

    bus.ram.data[0x1000] = 0x80  # Zero-page pointer address
    bus.ram.data[0x80] = 0xFF  # Low byte of target address
    bus.ram.data[0x81] = 0x12  # High byte of target address
    base_address = (0x12 << 8) | 0xFF  # Construct full address
    effective_address = (base_address + 0xF0) & 0xFFFF  # Account for Y
    bus.ram.data[effective_address] = 0x30  # Value in memory

    # Execute instruction
    heap.lda_indirect_y()

    # Expected values
    expected_value = 0x30
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but is {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 6, (
        "LDA (Indirect),Y instruction should take 6 cycles with page crossing"
    )
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_indirect_y, repeat=10000)

    log.info(
        f"[test_lda_indirect_y_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_absolute_non_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_absolute (LDA Absolute) instruction with a non-zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x34  # Low byte of address
    bus.ram.data[0x1001] = 0x12  # High byte of address
    address = (0x12 << 8) | 0x34  # Absolute address calculation
    bus.ram.data[address] = 0x45  # Value at the absolute address

    # Execute instruction
    heap.lda_absolute()

    # Expected results
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "LDA Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_absolute, repeat=10000)

    log.info(
        f"[test_lda_absolute_non_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_absolute_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_absolute (LDA Absolute) instruction with a zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0xFF  # Initial value of A
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Low byte of address
    bus.ram.data[0x1001] = 0x12  # High byte of address
    address = (0x12 << 8) | 0x50  # Absolute address calculation
    bus.ram.data[address] = 0x00  # Zero value at absolute address

    # Execute instruction
    heap.lda_absolute()

    # Expected results
    expected_value = 0x00
    expected_zero = True  # Since value is 0
    expected_negative = False  # Since bit 7 is not set

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "LDA Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_absolute, repeat=10000)

    log.info(
        f"[test_lda_absolute_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_immediate_non_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_immediate (LDA Immediate) instruction with a non-zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x45  # Immediate value to load

    # Execute instruction
    heap.lda_immediate()

    # Expected results
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "LDA Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_immediate, repeat=10000)

    log.info(
        f"[test_lda_immediate_non_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_immediate_zero(bus, heap, time_instruction) -> None:
    """Tests the lda_immediate (LDA Immediate) instruction with a zero value."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0xFF  # Initial value of A
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x00  # Immediate value to load

    # Execute instruction
    heap.lda_immediate()

    # Expected results
    expected_value = 0x00
    expected_zero = True  # Since value is 0
    expected_negative = False  # Since bit 7 is not set

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "LDA Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_immediate, repeat=10000)

    log.info(
        f"[test_lda_immediate_zero] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_absolute_x(bus, heap, time_instruction) -> None:
    """Tests the lda_absolute_x (LDA Absolute,X) instruction with and without page crossing."""
    # --- Setup test without page crossing ---
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x34  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    target_address = (base_address + bus.cpu.x) & 0xFFFF  # Effective address
    bus.ram.data[target_address] = 0x45  # Value at target address

    # Execute instruction
    heap.lda_absolute_x()

    # Expected results
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0
    expected_extra_cycle = 0  # No page crossing
    expected_cycles = 4 + expected_extra_cycle

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == expected_cycles, (
        f"LDA Absolute,X should take {expected_cycles} cycles"
    )
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_absolute_x, repeat=10000)

    log.info(
        f"[test_lda_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_absolute_x_page_cross(bus, heap, time_instruction) -> None:
    # --- Setup test with page crossing ---
    bus.cpu.pc = 0x2000
    bus.cpu.a = 0x00
    bus.cpu.x = 0xF5  # Large X offset to force page crossing

    bus.ram.data[0x2000] = 0xFF  # Low byte of base address
    bus.ram.data[0x2001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0xFF
    target_address = (
        base_address + bus.cpu.x
    ) & 0xFFFF  # Effective address with page crossing
    bus.ram.data[target_address] = 0x30  # Value at target address

    # Execute instruction
    heap.lda_absolute_x()

    # Expected results with page crossing
    expected_value = 0x30
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0
    expected_extra_cycle = 1  # Page crossing occurs
    expected_cycles = 4 + expected_extra_cycle

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == expected_cycles, (
        f"LDA Absolute,X should take {expected_cycles} cycles with page crossing"
    )
    assert bus.cpu.pc == 0x2002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_absolute_x, repeat=10000)

    log.info(
        f"[test_lda_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_absolute_y_no_page_cross(bus, heap, time_instruction) -> None:
    """Tests the lda_absolute_y (LDA Absolute,Y) instruction without page crossing."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.y = 0x05  # Y register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x34  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    effective_address = (base_address + bus.cpu.y) & 0xFFFF  # Effective address
    bus.ram.data[effective_address] = 0x45  # Value at effective address

    # Execute instruction
    heap.lda_absolute_y()

    # Expected results
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0
    expected_extra_cycle = 0  # No page crossing
    expected_cycles = 4 + expected_extra_cycle

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == expected_cycles, (
        f"LDA Absolute,Y should take {expected_cycles} cycles"
    )
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_absolute_y, repeat=10000)

    log.info(
        f"[test_lda_absolute_y_no_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lda_absolute_y_page_cross(bus, heap, time_instruction) -> None:
    """Tests the lda_absolute_y (LDA Absolute,Y) instruction with page crossing."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x00  # Initial value of A
    bus.cpu.y = 0xF5  # Large Y offset to force page crossing
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0xFF  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0xFF
    effective_address = (
        base_address + bus.cpu.y
    ) & 0xFFFF  # Effective address with page crossing
    bus.ram.data[effective_address] = 0x30  # Value at effective address

    # Execute instruction
    heap.lda_absolute_y()

    # Expected results
    expected_value = 0x30
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0
    expected_extra_cycle = 1  # Page crossing occurs
    expected_cycles = 4 + expected_extra_cycle

    # Verify results
    assert bus.cpu.a == expected_value, (
        f"A should be {hex(expected_value)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == expected_cycles, (
        f"LDA Absolute,Y should take {expected_cycles} cycles with page crossing"
    )
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.lda_absolute_y, repeat=10000)

    log.info(
        f"[test_lda_absolute_y_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sta_zeropage_x(bus, heap, time_instruction) -> None:
    """Tests the sta_zeropage_x (STA Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x55  # Value to store
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x80  # Base zero-page address
    effective_address = (0x80 + bus.cpu.x) & 0xFF  # Effective zero-page address

    # Execute instruction
    heap.sta_zeropage_x()

    # Verify results
    assert bus.ram.data[effective_address] == 0x55, (
        f"Memory at {hex(effective_address)} should be 0x55"
    )
    assert bus.cpu.cycles == 4, "STA Zero Page,X should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sta_zeropage_x, repeat=10000)

    log.info(
        f"[test_sta_zeropage_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sta_indirect_y(bus, heap, time_instruction) -> None:
    """Tests the sta_indirect_y (STA (Indirect),Y) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0xAA  # Value to store
    bus.cpu.y = 0x07  # Y register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x90  # Zero-page pointer
    bus.ram.data[0x90] = 0x20  # Low byte of base address
    bus.ram.data[0x91] = 0x30  # High byte of base address
    base_address = (0x30 << 8) | 0x20
    effective_address = (
        base_address + bus.cpu.y
    ) & 0xFFFF  # Effective address with Y offset

    # Execute instruction
    heap.sta_indirect_y()

    # Verify results
    assert bus.ram.data[effective_address] == 0xAA, (
        f"Memory at {hex(effective_address)} should be 0xAA"
    )
    assert bus.cpu.cycles == 6, "STA (Indirect),Y should take 6 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sta_indirect_y, repeat=10000)

    log.info(
        f"[test_sta_indirect_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sta_absolute_y(bus, heap, time_instruction) -> None:
    """Tests the sta_absolute_y (STA Absolute,Y) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x77  # Value to store
    bus.cpu.y = 0x10  # Y register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x40  # Low byte of base address
    bus.ram.data[0x1001] = 0x20  # High byte of base address
    base_address = (0x20 << 8) | 0x40
    target_address = (
        base_address + bus.cpu.y
    ) & 0xFFFF  # Effective address with Y offset

    # Execute instruction
    heap.sta_absolute_y()

    # Verify results
    assert bus.ram.data[target_address] == 0x77, (
        f"Memory at {hex(target_address)} should be 0x77"
    )
    assert bus.cpu.cycles == 5, "STA Absolute,Y should take 5 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sta_absolute_y, repeat=10000)

    log.info(
        f"[test_sta_absolute_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sta_absolute(bus, heap, time_instruction) -> None:
    """Tests the sta_absolute (STA Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x99  # Value to store
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x40  # Low byte of target address
    bus.ram.data[0x1001] = 0x20  # High byte of target address
    target_address = (0x20 << 8) | 0x40  # Absolute address

    # Execute instruction
    heap.sta_absolute()

    # Verify results
    assert bus.ram.data[target_address] == 0x99, (
        f"Memory at {hex(target_address)} should be 0x99"
    )
    assert bus.cpu.cycles == 4, "STA Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sta_absolute, repeat=10000)

    log.info(
        f"[test_sta_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sta_absolute_x(bus, heap, time_instruction) -> None:
    """Tests the sta_absolute_x (STA Absolute,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x77  # Value to store
    bus.cpu.x = 0x0A  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Low byte of base address
    bus.ram.data[0x1001] = 0x30  # High byte of base address
    base_address = (0x30 << 8) | 0x50
    effective_address = (
        base_address + bus.cpu.x
    ) & 0xFFFF  # Effective address with X offset

    # Execute instruction
    heap.sta_absolute_x()

    # Verify results
    assert bus.ram.data[effective_address] == 0x77, (
        f"Memory at {hex(effective_address)} should be 0x77"
    )
    assert bus.cpu.cycles == 5, "STA Absolute,X should take 5 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sta_absolute_x, repeat=10000)

    log.info(
        f"[test_sta_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldx_zero_page(bus, heap, time_instruction) -> None:
    """Tests the ldx_zero_page (LDX Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x00  # Initial value of X
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x45  # Value to load into X

    # Execute instruction
    heap.ldx_zero_page()

    # Expected results
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.x == expected_value, (
        f"X should be {hex(expected_value)}, but got {hex(bus.cpu.x)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "LDX Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldx_zero_page, repeat=10000)

    log.info(
        f"[test_ldx_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldx_absolute(bus, heap, time_instruction) -> None:
    """Tests the ldx_absolute (LDX Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x00  # Initial value of X
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Low byte of address
    bus.ram.data[0x1001] = 0x20  # High byte of address
    address = (0x20 << 8) | 0x50
    bus.ram.data[address] = 0xAA  # Value to load into X

    # Execute instruction
    heap.ldx_absolute()

    # Expected results
    expected_value = 0xAA
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.x == expected_value, (
        f"X should be {hex(expected_value)}, but got {hex(bus.cpu.x)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "LDX Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldx_absolute, repeat=10000)

    log.info(
        f"[test_ldx_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldx_immediate(bus, heap, time_instruction) -> None:
    """Tests the ldx_immediate (LDX Immediate) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x00  # Initial value of X
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x12  # Immediate value

    # Execute instruction
    heap.ldx_immediate()

    # Verify results
    assert bus.cpu.x == 0x12, "X register should hold 0x12"
    assert bus.cpu.cycles == 2, "LDX Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldx_immediate, repeat=10000)

    log.info(
        f"[test_ldx_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldx_absolute_y(bus, heap, time_instruction) -> None:
    """Tests the ldx_absolute_y (LDX Absolute,Y) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x00
    bus.cpu.y = 0x10  # Y register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0xF0  # Low byte of base address
    bus.ram.data[0x1001] = 0x30  # High byte of base address
    base_address = (0x30 << 8) | 0xF0
    effective_address = (base_address + bus.cpu.y) & 0xFFFF
    bus.ram.data[effective_address] = 0x99  # Value at effective address

    # Execute instruction
    heap.ldx_absolute_y()

    # Expected cycle count
    expected_extra_cycle = (
        1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
    )
    expected_cycles = 4 + expected_extra_cycle

    # Verify results
    assert bus.cpu.x == 0x99, "X register should hold 0x99"
    assert bus.cpu.cycles == expected_cycles, (
        f"LDX Absolute,Y should take {expected_cycles} cycles"
    )
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldx_absolute_y, repeat=10000)

    log.info(
        f"[test_ldx_absolute_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_stx_zero_page_y(bus, heap, time_instruction) -> None:
    """Tests the stx_zero_page_y (STX Zero Page,Y) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x77  # Value to store
    bus.cpu.y = 0x05  # Y register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x80  # Base zero-page address
    effective_address = (0x80 + bus.cpu.y) & 0xFF  # Effective zero-page address

    # Execute instruction
    heap.stx_zero_page_y()

    # Verify results
    assert bus.ram.data[effective_address] == 0x77, (
        f"Memory at {hex(effective_address)} should be 0x77"
    )
    assert bus.cpu.cycles == 4, "STX Zero Page,Y should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.stx_zero_page_y, repeat=10000)

    log.info(
        f"[test_stx_zero_page_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_stx_zero_page(bus, heap, time_instruction) -> None:
    """Tests the stx_zero_page (STX Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x99  # Value to store
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Target zero-page address

    # Execute instruction
    heap.stx_zero_page()

    # Verify results
    assert bus.ram.data[0x50] == 0x99, "Memory at 0x50 should be 0x99"
    assert bus.cpu.cycles == 3, "STX Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.stx_zero_page, repeat=10000)

    log.info(
        f"[test_stx_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_stx_absolute(bus, heap, time_instruction) -> None:
    """Tests the stx_absolute (STX Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x55  # Value to store
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x34  # Low byte of target address
    bus.ram.data[0x1001] = 0x12  # High byte of target address
    target_address = (0x12 << 8) | 0x34  # Absolute address

    # Execute instruction
    heap.stx_absolute()

    # Verify results
    assert bus.ram.data[target_address] == 0x55, (
        f"Memory at {hex(target_address)} should be 0x55"
    )
    assert bus.cpu.cycles == 4, "STX Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.stx_absolute, repeat=10000)

    log.info(
        f"[test_stx_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldy_zero_page(bus, heap, time_instruction) -> None:
    """Tests the ldy_zero_page (LDY Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x00  # Initial value of Y
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x45  # Value to load into Y

    # Execute instruction
    heap.ldy_zero_page()

    # Expected results
    expected_value = 0x45
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.y == expected_value, (
        f"Y should be {hex(expected_value)}, but got {hex(bus.cpu.y)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "LDY Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldy_zero_page, repeat=10000)

    log.info(
        f"[test_ldy_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldy_absolute(bus, heap, time_instruction) -> None:
    """Tests the ldy_absolute (LDY Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x00  # Initial value of Y
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Low byte of address
    bus.ram.data[0x1001] = 0x20  # High byte of address
    address = (0x20 << 8) | 0x50
    bus.ram.data[address] = 0xAA  # Value to load into Y

    # Execute instruction
    heap.ldy_absolute()

    # Expected results
    expected_value = 0xAA
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.cpu.y == expected_value, (
        f"Y should be {hex(expected_value)}, but got {hex(bus.cpu.y)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "LDY Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldy_absolute, repeat=10000)

    log.info(
        f"[test_ldy_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldy_immediate(bus, heap, time_instruction) -> None:
    """Tests the ldy_immediate (LDY Immediate) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x00  # Initial value of Y
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x12  # Immediate value

    # Execute instruction
    heap.ldy_immediate()

    # Verify results
    assert bus.cpu.y == 0x12, "Y register should hold 0x12"
    assert bus.cpu.cycles == 2, "LDY Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldy_immediate, repeat=10000)

    log.info(
        f"[test_ldy_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ldy_absolute_x(bus, heap, time_instruction) -> None:
    """Tests the ldy_absolute_x (LDY Absolute,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x00
    bus.cpu.x = 0x10  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0xF0  # Low byte of base address
    bus.ram.data[0x1001] = 0x30  # High byte of base address
    base_address = (0x30 << 8) | 0xF0
    effective_address = (base_address + bus.cpu.x) & 0xFFFF
    bus.ram.data[effective_address] = 0x99  # Value at effective address

    # Execute instruction
    heap.ldy_absolute_x()

    # Expected cycle count
    expected_extra_cycle = (
        1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
    )
    expected_cycles = 4 + expected_extra_cycle

    # Verify results
    assert bus.cpu.y == 0x99, "Y register should hold 0x99"
    assert bus.cpu.cycles == expected_cycles, (
        f"LDY Absolute,X should take {expected_cycles} cycles"
    )
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.ldy_absolute_x, repeat=10000)

    log.info(
        f"[test_ldy_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sty_absolute(bus, heap, time_instruction) -> None:
    """Tests the sty_absolute (STY Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x77  # Value to store
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x34  # Low byte of target address
    bus.ram.data[0x1001] = 0x12  # High byte of target address
    target_address = (0x12 << 8) | 0x34  # Absolute address

    # Execute instruction
    heap.sty_absolute()

    # Verify results
    assert bus.ram.data[target_address] == 0x77, (
        f"Memory at {hex(target_address)} should be 0x77"
    )
    assert bus.cpu.cycles == 4, "STY Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sty_absolute, repeat=10000)

    log.info(
        f"[test_sty_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sty_zero_page_x(bus, heap, time_instruction) -> None:
    """Tests the sty_zero_page_x (STY Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x99  # Value to store
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x80  # Base zero-page address
    target_address = (0x80 + bus.cpu.x) & 0xFF  # Effective zero-page address

    # Execute instruction
    heap.sty_zero_page_x()

    # Verify results
    assert bus.ram.data[target_address] == 0x99, (
        f"Memory at {hex(target_address)} should be 0x99"
    )
    assert bus.cpu.cycles == 4, "STY Zero Page,X should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sty_zero_page_x, repeat=10000)

    log.info(
        f"[test_sty_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_sty_zero_page(bus, heap, time_instruction) -> None:
    """Tests the sty_zero_page (STY Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x55  # Value to store
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Target zero-page address

    # Execute instruction
    heap.sty_zero_page()

    # Verify results
    assert bus.ram.data[0x50] == 0x55, "Memory at 0x50 should be 0x55"
    assert bus.cpu.cycles == 3, "STY Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.sty_zero_page, repeat=10000)

    log.info(
        f"[test_sty_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_dec_zero_page(bus, heap, time_instruction) -> None:
    """Tests the dec_zero_page (DEC Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x05  # Initial value at zero-page address

    # Execute instruction
    heap.dec_zero_page()

    # Expected results
    expected_value = 0x04
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.ram.data[0x80] == expected_value, (
        f"Memory at 0x80 should be {hex(expected_value)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5, "DEC Zero Page should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.dec_zero_page, repeat=10000)

    log.info(
        f"[test_dec_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_dec_absolute(bus, heap, time_instruction) -> None:
    """Tests the dec_absolute (DEC Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Low byte of address
    bus.ram.data[0x1001] = 0x20  # High byte of address
    address = (0x20 << 8) | 0x50
    bus.ram.data[address] = 0x10  # Initial value at absolute address

    # Execute instruction
    heap.dec_absolute()

    # Expected results
    expected_value = 0x0F
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.ram.data[address] == expected_value, (
        f"Memory at {hex(address)} should be {hex(expected_value)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 6, "DEC Absolute should take 6 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.dec_absolute, repeat=10000)

    log.info(
        f"[test_dec_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_inc_absolute_x(bus, heap, time_instruction) -> None:
    """Tests the inc_absolute_x (INC Absolute,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Low byte of base address
    bus.ram.data[0x1001] = 0x20  # High byte of base address
    base_address = (0x20 << 8) | 0x50
    target_address = (base_address + bus.cpu.x) & 0xFFFF  # Effective address
    bus.ram.data[target_address] = 0x7E  # Initial value at memory location

    # Execute instruction
    heap.inc_absolute_x()

    # Expected results
    expected_value = 0x7F
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.ram.data[target_address] == expected_value, (
        f"Memory at {hex(target_address)} should be {hex(expected_value)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 7, "INC Absolute,X should take 7 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.inc_absolute_x, repeat=10000)

    log.info(
        f"[test_inc_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_inc_zero_page_x(bus, heap, time_instruction) -> None:
    """Tests the inc_zero_page_x (INC Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x04  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x30  # Base zero-page address
    effective_address = (0x30 + bus.cpu.x) & 0xFF  # Effective zero-page address
    bus.ram.data[effective_address] = 0xFF  # Initial value at memory location

    # Execute instruction
    heap.inc_zero_page_x()

    # Expected results
    expected_value = 0x00  # Wrap-around
    expected_zero = True
    expected_negative = False

    # Verify results
    assert bus.ram.data[effective_address] == expected_value, (
        f"Memory at {hex(effective_address)} should be {hex(expected_value)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 6, "INC Zero Page,X should take 6 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.inc_zero_page_x, repeat=10000)

    log.info(
        f"[test_inc_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_inc_zero_page(bus, heap, time_instruction) -> None:
    """Tests the inc_zero_page (INC Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Zero-page address
    bus.ram.data[0x50] = 0x10  # Initial value at zero-page address

    # Execute instruction
    heap.inc_zero_page()

    # Expected results
    expected_value = 0x11
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.ram.data[0x50] == expected_value, (
        f"Memory at 0x50 should be {hex(expected_value)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5, "INC Zero Page should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.inc_zero_page, repeat=10000)

    log.info(
        f"[test_inc_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_inc_absolute(bus, heap, time_instruction) -> None:
    """Tests the inc_absolute (INC Absolute) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x20  # Low byte of address
    bus.ram.data[0x1001] = 0x30  # High byte of address
    target_address = (0x30 << 8) | 0x20
    bus.ram.data[target_address] = 0x80  # Initial value at memory location

    # Execute instruction
    heap.inc_absolute()

    # Expected results
    expected_value = 0x81
    expected_zero = expected_value == 0
    expected_negative = (expected_value & 0x80) != 0

    # Verify results
    assert bus.ram.data[target_address] == expected_value, (
        f"Memory at {hex(target_address)} should be {hex(expected_value)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 6, "INC Absolute should take 6 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(heap.inc_absolute, repeat=10000)

    log.info(
        f"[test_inc_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )
