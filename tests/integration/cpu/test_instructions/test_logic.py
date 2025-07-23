import pytest

from src.cpu.instructions.logic import Logic
from src.utils.log_setup import log


@pytest.fixture
def logic(bus):
    return Logic(bus.cpu)


def test_and_indirect_y(bus, logic, time_instruction) -> None:
    """Tests the and_indirect_y (AND Indirect,Y) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x04  # Y register offset
    bus.cpu.a = 0xF0  # Initial A register value

    bus.ram.data[0x1000] = 0x20  # Zero-page address
    bus.ram.data[0x20] = 0x50  # Low byte of base address
    bus.ram.data[0x21] = 0x40  # High byte of base address
    effective_address = ((0x40 << 8) | 0x50) + bus.cpu.y  # Address after Y offset
    bus.ram.data[effective_address] = 0x0F  # Memory value for AND operation

    # Execute instruction
    logic.and_indirect_y()

    # Expected results
    expected_result = 0xF0 & 0x0F
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5, "AND Indirect,Y should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.and_indirect_y, repeat=10000)

    log.info(
        f"[test_and_indirect_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_and_immediate(bus, logic, time_instruction) -> None:
    """Tests the and_immediate (AND Immediate) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0xAA  # Initial A register value

    bus.ram.data[0x1000] = 0x55  # Immediate value for AND operation

    # Execute instruction
    logic.and_immediate()

    # Expected results
    expected_result = 0xAA & 0x55
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "AND Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.and_immediate, repeat=10000)

    log.info(
        f"[test_and_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_and_zero_page(bus, logic, time_instruction) -> None:
    """Tests the and_zero_page (AND Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x3C  # Initial A register value

    bus.ram.data[0x1000] = 0x40  # Zero-page address
    bus.ram.data[0x40] = 0x0F  # Memory value for AND operation

    # Execute instruction
    logic.and_zero_page()

    # Expected results
    expected_result = 0x3C & 0x0F
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "AND Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.and_zero_page, repeat=10000)

    log.info(
        f"[test_and_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_asl_accumulator(bus, logic, time_instruction) -> None:
    """Tests the asl_accumulator (Arithmetic Shift Left on Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x81  # Initial A register value (10000001 in binary)
    bus.cpu.status = 0x00  # Clear status flags

    # Execute instruction
    logic.asl_accumulator()

    # Expected results
    expected_result = (0x81 << 1) & 0xFF  # Expected shifted value: 0x02
    expected_carry = 1  # Carry should be set since bit 7 was 1
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "ASL Accumulator should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.asl_accumulator, repeat=10000)

    log.info(
        f"[test_asl_accumulator] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_asl_zero_page(bus, logic, time_instruction) -> None:
    """Tests the asl_zero_page (Arithmetic Shift Left on Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Zero-page address
    bus.ram.data[0x50] = 0x40  # Initial memory value (01000000 in binary)

    # Execute instruction
    logic.asl_zero_page()

    # Expected results
    expected_result = (0x40 << 1) & 0xFF  # Expected shifted value: 0x80
    expected_carry = 0  # Carry should not be set since bit 7 was 0
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.ram.data[0x50] == expected_result, (
        f"Memory at 0x50 should be {hex(expected_result)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5, "ASL Zero Page should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.asl_zero_page, repeat=10000)

    log.info(
        f"[test_asl_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_asl_zero_page_x(bus, logic, time_instruction) -> None:
    """Tests the asl_zero_page_x (Arithmetic Shift Left on Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x30  # Base zero-page address
    effective_address = (0x30 + bus.cpu.x) & 0xFF  # Effective address after X indexing
    bus.ram.data[effective_address] = 0xFF  # Initial memory value (11111111 in binary)

    # Execute instruction
    logic.asl_zero_page_x()

    # Expected results
    expected_result = (0xFF << 1) & 0xFF  # Expected shifted value: 0xFE
    expected_carry = 1  # Carry should be set since bit 7 was 1
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.ram.data[effective_address] == expected_result, (
        f"Memory at {hex(effective_address)} should be {hex(expected_result)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 6, "ASL Zero Page,X should take 6 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.asl_zero_page_x, repeat=10000)

    log.info(
        f"[test_asl_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_eor_zero_page_x(bus, logic, time_instruction) -> None:
    """Tests the eor_zero_page_x (EOR Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.a = 0xAA  # Initial A register value

    bus.ram.data[0x1000] = 0x20  # Base zero-page address
    effective_address = (0x20 + bus.cpu.x) & 0xFF  # Effective address after X offset
    bus.ram.data[effective_address] = 0x55  # Memory value for XOR operation

    # Execute instruction
    logic.eor_zero_page_x()

    # Expected results
    expected_result = 0xAA ^ 0x55
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "EOR Zero Page,X should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.eor_zero_page_x, repeat=10000)

    log.info(
        f"[test_eor_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_eor_immediate(bus, logic, time_instruction) -> None:
    """Tests the eor_immediate (EOR Immediate) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x0F  # Initial A register value

    bus.ram.data[0x1000] = 0xF0  # Immediate value for XOR operation

    # Execute instruction
    logic.eor_immediate()

    # Expected results
    expected_result = 0x0F ^ 0xF0
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "EOR Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.eor_immediate, repeat=10000)

    log.info(
        f"[test_eor_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_eor_indirect_x(bus, logic, time_instruction) -> None:
    """Tests the eor_indirect_x (EOR Indirect,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x04  # X register offset
    bus.cpu.a = 0x3C  # Initial A register value

    bus.ram.data[0x1000] = 0x10  # Base zero-page address
    effective_address = (0x10 + bus.cpu.x) & 0xFF  # Effective zero-page address
    bus.ram.data[effective_address] = 0x50  # Low byte of target address
    bus.ram.data[(effective_address + 1) & 0xFF] = 0x40  # High byte of target address
    target_address = (0x40 << 8) | 0x50  # Full 16-bit target address
    bus.ram.data[target_address] = 0x0F  # Memory value for XOR operation

    # Execute instruction
    logic.eor_indirect_x()

    # Expected results
    expected_result = 0x3C ^ 0x0F
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 6, "EOR Indirect,X should take 6 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.eor_indirect_x, repeat=10000)

    log.info(
        f"[test_eor_indirect_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lsr_accumulator(bus, logic, time_instruction) -> None:
    """Tests the lsr_accumulator (Logical Shift Right on Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x81  # Initial A register value (10000001 in binary)
    bus.cpu.status = 0x00  # Clear status flags

    # Execute instruction
    logic.lsr_accumulator()

    # Expected results
    expected_result = (0x81 >> 1) & 0xFF  # Expected shifted value: 0x40
    expected_carry = 0x81 & 0x01  # Carry should be set since bit 0 was 1
    expected_zero = expected_result == 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == 0x00, "Negative flag should always be 0 for LSR"
    assert bus.cpu.cycles == 2, "LSR Accumulator should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.lsr_accumulator, repeat=10000)

    log.info(
        f"[test_lsr_accumulator] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_lsr_zero_page(bus, logic, time_instruction) -> None:
    """Tests the lsr_zero_page (Logical Shift Right on Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x50  # Zero-page address
    bus.ram.data[0x50] = 0x02  # Initial memory value (00000010 in binary)

    # Execute instruction
    logic.lsr_zero_page()

    # Expected results
    expected_result = (0x02 >> 1) & 0xFF  # Expected shifted value: 0x01
    expected_carry = 0x02 & 0x01  # Carry should be 0 (since bit 0 was 0)
    expected_zero = expected_result == 0

    # Verify results
    assert bus.ram.data[0x50] == expected_result, (
        f"Memory at 0x50 should be {hex(expected_result)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == 0x00, "Negative flag should always be 0 for LSR"
    assert bus.cpu.cycles == 5, "LSR Zero Page should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.lsr_zero_page, repeat=10000)

    log.info(
        f"[test_lsr_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ora_zero_page(bus, logic, time_instruction) -> None:
    """Tests the ora_zero_page (Logical OR with Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x12  # Initial A register value

    bus.ram.data[0x1000] = 0x30  # Zero-page address
    bus.ram.data[0x30] = 0x34  # Memory value for OR operation

    # Execute instruction
    logic.ora_zero_page()

    # Expected results
    expected_result = 0x12 | 0x34
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "ORA Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ora_zero_page, repeat=10000)

    log.info(
        f"[test_ora_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ora_absolute(bus, logic, time_instruction) -> None:
    """Tests the ora_absolute (Logical OR with Absolute Addressing) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x0F  # Initial A register value

    bus.ram.data[0x1000] = 0x50  # Low byte of address
    bus.ram.data[0x1001] = 0x20  # High byte of address
    absolute_address = (0x20 << 8) | 0x50
    bus.ram.data[absolute_address] = 0xF0  # Memory value for OR operation

    # Execute instruction
    logic.ora_absolute()

    # Expected results
    expected_result = 0x0F | 0xF0
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 4, "ORA Absolute should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should increment by 2"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ora_absolute, repeat=10000)

    log.info(
        f"[test_ora_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ora_immediate(bus, logic, time_instruction) -> None:
    """Tests the ora_immediate (Logical OR with Immediate Value) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x44  # Initial A register value

    bus.ram.data[0x1000] = 0x22  # Immediate value for OR operation

    # Execute instruction
    logic.ora_immediate()

    # Expected results
    expected_result = 0x44 | 0x22
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "ORA Immediate should take 2 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ora_immediate, repeat=10000)

    log.info(
        f"[test_ora_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ora_indirect_indexed(bus, logic, time_instruction) -> None:
    """Tests the ora_indirect_indexed (Logical OR with Indirect Indexed Addressing) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x05  # Y register offset
    bus.cpu.a = 0x10  # Initial A register value

    bus.ram.data[0x1000] = 0x40  # Zero-page address
    base_address = (0x20 << 8) | 0x30
    effective_address = (base_address + bus.cpu.y) & 0xFFFF

    bus.ram.data[0x40] = 0x30  # Low byte of base address
    bus.ram.data[0x41] = 0x20  # High byte of base address
    bus.ram.data[effective_address] = 0xC0  # Memory value for OR operation

    # Execute instruction
    logic.ora_indirect_indexed()

    # Expected results
    expected_result = 0x10 | 0xC0
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5 + (
        1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
    ), "ORA Indirect Indexed should take correct cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ora_indirect_indexed, repeat=10000)

    log.info(
        f"[test_ora_indirect_indexed] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_rol_accumulator(bus, logic, time_instruction) -> None:
    """Tests the rol_accumulator (Rotate Left on Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0b10000001  # Initial A register value
    bus.cpu.status = 0x01  # Carry flag set

    # Execute instruction
    logic.rol_accumulator()

    # Expected results
    expected_result = (
        (0b10000001 << 1) | 1
    ) & 0xFF  # Expected rotated value: 0b00000011 (0x03)
    expected_carry = (0b10000001 & 0x80) >> 7  # Should set carry flag to 1
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {bin(expected_result)}, but got {bin(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "ROL Accumulator should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.rol_accumulator, repeat=10000)

    log.info(
        f"[test_rol_accumulator] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_rol_zero_page(bus, logic, time_instruction) -> None:
    """Tests the rol_zero_page (Rotate Left on Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags, Carry = 0

    bus.ram.data[0x1000] = 0x50  # Zero-page address
    bus.ram.data[0x50] = 0b01010101  # Initial memory value

    # Execute instruction
    logic.rol_zero_page()

    # Expected results
    expected_result = (
        (0b01010101 << 1) | 0
    ) & 0xFF  # Expected rotated value: 0b10101010 (0xAA)
    expected_carry = (0b01010101 & 0x80) >> 7  # Carry should be 0
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0  # Should be 1

    # Verify results
    assert bus.ram.data[0x50] == expected_result, (
        f"Memory at 0x50 should be {bin(expected_result)}, but got {bin(bus.ram.data[0x50])}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 5, "ROL Zero Page should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.rol_zero_page, repeat=10000)

    log.info(
        f"[test_rol_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ror_accumulator(bus, logic, time_instruction) -> None:
    """Tests the ror_accumulator (Rotate Right on Accumulator) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0b10000001  # Initial A register value
    bus.cpu.status = 0x01  # Carry flag set

    # Execute instruction
    logic.ror_accumulator()

    # Expected results
    expected_result = (
        (0b10000001 >> 1) | (1 << 7)
    ) & 0xFF  # Expected rotated value: 0b11000000 (0xC0)
    expected_carry = 0b10000001 & 0x01  # Should set carry flag to 1
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {bin(expected_result)}, but got {bin(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 2, "ROR Accumulator should take 2 cycles"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ror_accumulator, repeat=10000)

    log.info(
        f"[test_ror_accumulator] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ror_zero_page(bus, logic, time_instruction) -> None:
    """Tests the ror_zero_page (Rotate Right on Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags, Carry = 0

    bus.ram.data[0x1000] = 0x50  # Zero-page address
    bus.ram.data[0x50] = 0b01010101  # Initial memory value

    # Execute instruction
    logic.ror_zero_page()

    # Expected results
    expected_result = (
        (0b01010101 >> 1) | (0 << 7)
    ) & 0xFF  # Expected rotated value: 0b00101010 (0x2A)
    expected_carry = 0b01010101 & 0x01  # Carry should be 1
    expected_zero = expected_result == 0

    # Verify results
    assert bus.ram.data[0x50] == expected_result, (
        f"Memory at 0x50 should be {bin(expected_result)}, but got {bin(bus.ram.data[0x50])}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == 0x00, "Negative flag incorrect"
    assert bus.cpu.cycles == 5, "ROR Zero Page should take 5 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ror_zero_page, repeat=10000)

    log.info(
        f"[test_ror_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ror_zero_page_x(bus, logic, time_instruction) -> None:
    """Tests the ror_zero_page_x (Rotate Right on Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags, Carry = 0

    bus.ram.data[0x1000] = 0x40  # Base zero-page address
    effective_address = (0x40 + bus.cpu.x) & 0xFF  # Effective address after X offset
    bus.ram.data[effective_address] = 0b11001100  # Initial memory value

    # Execute instruction
    logic.ror_zero_page_x()

    # Expected results
    expected_result = (
        (0b11001100 >> 1) | (0 << 7)
    ) & 0xFF  # Expected rotated value: 0b01100110 (0x66)
    expected_carry = 0b11001100 & 0x01  # Carry should be 0
    expected_zero = expected_result == 0

    # Verify results
    assert bus.ram.data[effective_address] == expected_result, (
        f"Memory at {hex(effective_address)} should be {bin(expected_result)},"
        f" but got {bin(bus.ram.data[effective_address])}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == 0x00, "Negative flag incorrect"
    assert bus.cpu.cycles == 6, "ROR Zero Page,X should take 6 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.ror_zero_page_x, repeat=10000)

    log.info(
        f"[test_ror_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_ror_absolute(bus, logic, time_instruction) -> None:
    """Tests the ror_absolute (Rotate Right on Absolute Addressing) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear status flags, Carry = 0

    bus.ram.data[0x1000] = 0x20  # Low byte of address
    bus.ram.data[0x1001] = 0x30  # High byte of address
    absolute_address = (0x30 << 8) | 0x20
    bus.ram.data[absolute_address] = 0b00001111  # Initial memory value

    # Execute instruction
    logic.ror_absolute()

    # Expected results
    expected_result = (
        (0b00001111 >> 1) | (0 << 7)
    ) & 0xFF  # Expected rotated value: 0b00000111 (0x07)

    # Verify results
    assert bus.ram.data[absolute_address] == expected_result, (
        f"Memory at {hex(absolute_address)} should be {bin(expected_result)}, "
        f"but got {bin(bus.ram.data[absolute_address])}"
    )


def test_lsr_zero_page_x(bus, logic, time_instruction) -> None:
    """Tests the lsr_zero_page_x (Logical Shift Right on Zero Page,X) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status = 0x00  # Clear status flags

    bus.ram.data[0x1000] = 0x20  # Base zero-page address
    effective_address = (0x20 + bus.cpu.x) & 0xFF  # Effective address after X offset
    bus.ram.data[effective_address] = 0b10101010  # Initial memory value

    # Execute instruction
    logic.lsr_zero_page_x()

    # Expected results
    expected_result = (
        0b10101010 >> 1
    ) & 0xFF  # Expected shifted value: 0b01010101 (0x55)
    expected_carry = 0b10101010 & 0x01  # Carry should be 0
    expected_zero = expected_result == 0

    # Verify results
    assert bus.ram.data[effective_address] == expected_result, (
        f"Memory at {hex(effective_address)} should be {bin(expected_result)}, "
        f"but got {bin(bus.ram.data[effective_address])}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == 0x00, "Negative flag incorrect"
    assert bus.cpu.cycles == 6, "LSR Zero Page,X should take 6 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.lsr_zero_page_x, repeat=10000)

    log.info(
        f"[test_lsr_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_eor_zero_page(bus, logic, time_instruction) -> None:
    """Tests the eor_zero_page (Exclusive OR with Zero Page) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x3C  # Initial A register value

    bus.ram.data[0x1000] = 0x40  # Zero-page address
    bus.ram.data[0x40] = 0x0F  # Memory value for XOR operation

    # Execute instruction
    logic.eor_zero_page()

    # Expected results
    expected_result = 0x3C ^ 0x0F
    expected_zero = expected_result == 0
    expected_negative = (expected_result & 0x80) != 0

    # Verify results
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )
    assert bus.cpu.cycles == 3, "EOR Zero Page should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should increment by 1"

    # Measure execution time
    total_time, avg_time = time_instruction(logic.eor_zero_page, repeat=10000)

    log.info(
        f"[test_eor_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )
