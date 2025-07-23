import pytest

from src.cpu.instructions.arithmetic import Arithmetic
from src.utils.log_setup import log


@pytest.fixture
def arithmetic(bus):
    return Arithmetic(bus.cpu)


def test_sbc_immediate(bus, arithmetic, time_instruction) -> None:
    """Tests the sbc_immediate instruction and measures its execution time."""
    # Ustawienia początkowe CPU i pamięci
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Akumulator początkowo 0x50
    bus.cpu.status = (bus.cpu.status | 0x01) & ~(
        1 << 3
    )  # Ustawienie Carry, wyczyszczenie Decimal Mode
    bus.ram.data[0x1000] = 0x20  # Wartość do odjęcia

    # Test dla trybu binarnego (Decimal Mode = False)
    arithmetic.sbc_immediate()

    # Sprawdzanie wyniku
    assert bus.cpu.a == 0x30, (
        "Akumulator powinien wynosić 0x30 po SBC w trybie binarnym"
    )
    assert (bus.cpu.status & 0x01) == 0x01, (
        "Flaga Carry powinna być ustawiona, gdy wynik jest nieujemny"
    )
    assert (bus.cpu.status & 0x02) == 0x00, (
        "Flaga Zero nie powinna być ustawiona, gdy wynik nie jest równy zero"
    )
    assert (bus.cpu.status & 0x80) == 0x00, (
        "Flaga Negative nie powinna być ustawiona, gdy wynik nie jest ujemny"
    )
    assert (bus.cpu.status & 0x40) == 0x00, (
        "Flaga Overflow nie powinna być ustawiona, gdy nie wystąpiło przepełnienie"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_immediate, repeat=10000)

    log.info(
        f"[test_sbc_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_sbc_absolute_x(bus, arithmetic, time_instruction) -> None:
    """Tests the sbc_absolute_x instruction and measures its execution time."""
    # Ustawienia początkowe CPU i pamięci
    bus.cpu.pc = 0x1000  # Ustawienie PC na adres 0x1000
    bus.cpu.x = 0x10  # Ustawienie rejestru X na 0x10
    bus.cpu.a = 0x50  # Akumulator początkowo 0x50
    bus.cpu.status = (bus.cpu.status | 0x01) & ~(
        1 << 3
    )  # Ustawienie Carry, wyczyszczenie Decimal Mode
    bus.ram.data[0x1000] = 0x00  # LSB adresu docelowego
    bus.ram.data[0x1001] = 0x20  # MSB adresu docelowego (adres docelowy to 0x2000)
    bus.ram.data[0x2010] = 0x20  # Wartość w pamięci pod adresem 0x2000 + X (0x2010)

    # Test dla trybu binarnego (Decimal Mode = False)
    arithmetic.sbc_absolute_x()

    # Sprawdzanie wyniku
    assert bus.cpu.a == 0x30, (
        "Akumulator powinien wynosić 0x30 po SBC w trybie binarnym"
    )
    assert (bus.cpu.status & 0x01) == 0x01, (
        "Flaga Carry powinna być ustawiona, gdy wynik jest nieujemny"
    )
    assert (bus.cpu.status & 0x02) == 0x00, (
        "Flaga Zero nie powinna być ustawiona, gdy wynik nie jest równy zero"
    )
    assert (bus.cpu.status & 0x80) == 0x00, (
        "Flaga Negative nie powinna być ustawiona, gdy wynik nie jest ujemny"
    )
    assert (bus.cpu.status & 0x40) == 0x00, (
        "Flaga Overflow nie powinna być ustawiona, gdy nie wystąpiło przepełnienie"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_absolute_x, repeat=10000)

    log.info(
        f"[test_sbc_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_sbc_absolute_y(bus, arithmetic, time_instruction) -> None:
    """Tests the sbc_absolute_y instruction and measures its execution time."""
    # Ustawienia początkowe CPU i pamięci
    bus.cpu.pc = 0x1000  # Ustawienie PC na adres 0x1000
    bus.cpu.y = 0x10  # Ustawienie rejestru Y na 0x10
    bus.cpu.a = 0x50  # Akumulator początkowo 0x50
    bus.cpu.status = (bus.cpu.status | 0x01) & ~(
        1 << 3
    )  # Ustawienie Carry, wyczyszczenie Decimal Mode
    bus.ram.data[0x1000] = 0x00  # LSB adresu bazowego
    bus.ram.data[0x1001] = 0x20  # MSB adresu bazowego (adres bazowy to 0x2000)
    bus.ram.data[0x2010] = 0x20  # Wartość w pamięci pod adresem 0x2000 + Y (0x2010)

    # Test dla trybu binarnego (Decimal Mode = False)
    arithmetic.sbc_absolute_y()

    # Sprawdzanie wyniku
    assert bus.cpu.a == 0x30, (
        "Akumulator powinien wynosić 0x30 po SBC w trybie binarnym"
    )
    assert (bus.cpu.status & 0x01) == 0x01, (
        "Flaga Carry powinna być ustawiona, gdy wynik jest nieujemny"
    )
    assert (bus.cpu.status & 0x02) == 0x00, (
        "Flaga Zero nie powinna być ustawiona, gdy wynik nie jest równy zero"
    )
    assert (bus.cpu.status & 0x80) == 0x00, (
        "Flaga Negative nie powinna być ustawiona, gdy wynik nie jest ujemny"
    )
    assert (bus.cpu.status & 0x40) == 0x00, (
        "Flaga Overflow nie powinna być ustawiona, gdy nie wystąpiło przepełnienie"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_absolute_y, repeat=10000)

    log.info(
        f"[test_sbc_absolute_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_sbc_zero_page(bus, arithmetic, time_instruction) -> None:
    """
    Tests the sbc_zero_page (SBC Zero Page) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.status |= 0x01  # Set carry flag (Bit 0)
    bus.ram.data[0x1000] = 0x80  # Address in zero-page
    bus.ram.data[0x80] = 0x30  # Value at zero-page address

    # First, test functionality:
    arithmetic.sbc_zero_page()

    expected_result = 0x50 - 0x30  # Expected result with carry included
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert bus.cpu.cycles == 3, "SBC Zero Page instruction should take 3 cycles"
    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    # Checking flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_result >= 0 else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_result == 0 else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if (expected_result & 0x80) else 0x00), (
        "Negative flag incorrect"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_zero_page, repeat=10000)

    log.info(
        f"[test_sbc_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_sbc_absolute(bus, arithmetic, time_instruction) -> None:
    """
    Tests the sbc_absolute (SBC Absolute) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.status |= 0x01  # Set carry flag (Bit 0)
    bus.ram.data[0x1000] = 0x34  # Low byte of the address
    bus.ram.data[0x1001] = 0x12  # High byte of the address
    bus.ram.data[0x1234] = 0x30  # Value at the absolute address

    # First, test functionality:
    arithmetic.sbc_absolute()

    expected_result = 0x50 - 0x30  # Expected result with carry included
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert bus.cpu.cycles == 4, "SBC Absolute instruction should take 4 cycles"
    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    # Checking flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_result >= 0 else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_result == 0 else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if (expected_result & 0x80) else 0x00), (
        "Negative flag incorrect"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_absolute, repeat=10000)

    log.info(
        f"[test_sbc_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_sbc_zero_page_x(bus, arithmetic, time_instruction) -> None:
    """
    Tests the sbc_zero_page_x (SBC Zero Page,X) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.x = 0x05  # X register offset
    bus.cpu.status |= 0x01  # Set carry flag (Bit 0)
    bus.ram.data[0x1000] = 0x80  # Base zero-page address
    bus.ram.data[(0x80 + 0x05) & 0xFF] = 0x30  # Value at (zero-page + X) address

    # First, test functionality:
    arithmetic.sbc_zero_page_x()

    expected_result = 0x50 - 0x30  # Expected result with carry included
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )
    assert bus.cpu.cycles == 4, "SBC Zero Page,X instruction should take 4 cycles"
    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    # Checking flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_result >= 0 else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_result == 0 else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if (expected_result & 0x80) else 0x00), (
        "Negative flag incorrect"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_zero_page_x, repeat=10000)

    log.info(
        f"[test_sbc_zero_page_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_sbc_indirect_y(bus, arithmetic, time_instruction) -> None:
    """
    Tests the sbc_indirect_y (SBC (Indirect),Y) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.y = 0x05  # Y register offset
    bus.cpu.status |= 0x01  # Set carry flag (Bit 0)

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x34  # Low byte of base address
    bus.ram.data[0x81] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    effective_address = (base_address + 0x05) & 0xFFFF  # Applying Y offset
    bus.ram.data[effective_address] = 0x30  # Value at the effective address

    # First, test functionality:
    arithmetic.sbc_indirect_y()

    expected_result = 0x50 - 0x30  # Expected result with carry included
    assert bus.cpu.a == expected_result, (
        f"A should be {hex(expected_result)}, but got {hex(bus.cpu.a)}"
    )

    # Check cycle count, accounting for page crossing
    page_crossed = (base_address & 0xFF00) != (effective_address & 0xFF00)
    expected_cycles = 5 + (1 if page_crossed else 0)
    assert bus.cpu.cycles == expected_cycles, (
        f"SBC (Indirect),Y instruction should take {expected_cycles} cycles"
    )

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    # Checking flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_result >= 0 else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_result == 0 else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if (expected_result & 0x80) else 0x00), (
        "Negative flag incorrect"
    )

    total_time, avg_time = time_instruction(arithmetic.sbc_indirect_y, repeat=10000)

    log.info(
        f"[test_sbc_indirect_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cmp_indirect_y(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cmp_indirect_y (CMP (Indirect),Y) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.y = 0x05  # Y register offset

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x34  # Low byte of base address
    bus.ram.data[0x81] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    effective_address = (base_address + 0x05) & 0xFFFF  # Applying Y offset
    bus.ram.data[effective_address] = 0x30  # Value at the effective address

    # First, test functionality:
    arithmetic.cmp_indirect_y()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count, accounting for page crossing
    page_crossed = (base_address & 0xFF00) != (effective_address & 0xFF00)
    expected_cycles = 5 + (1 if page_crossed else 0)
    assert bus.cpu.cycles == expected_cycles, (
        f"CMP (Indirect),Y instruction should take {expected_cycles} cycles"
    )

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cmp_indirect_y, repeat=10000)

    log.info(
        f"[test_cmp_indirect_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cmp_absolute_y(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cmp_absolute_y (CMP Absolute,Y) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.y = 0x05  # Y register offset

    bus.ram.data[0x1000] = 0x34  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    target_address = (base_address + 0x05) & 0xFFFF  # Applying Y offset
    bus.ram.data[target_address] = 0x30  # Value at the target address

    # First, test functionality:
    arithmetic.cmp_absolute_y()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count, accounting for page crossing
    page_crossed = (base_address & 0xFF00) != (target_address & 0xFF00)
    expected_cycles = 4 + (1 if page_crossed else 0)
    assert bus.cpu.cycles == expected_cycles, (
        f"CMP Absolute,Y instruction should take {expected_cycles} cycles"
    )

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.cmp_absolute_y, repeat=10000)

    log.info(
        f"[test_cmp_absolute_y] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cmp_zero_page(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cmp_zero_page (CMP Zero Page) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x30  # Value at the zero-page address

    # First, test functionality:
    arithmetic.cmp_zero_page()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 3, "CMP Zero Page instruction should take 3 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cmp_zero_page, repeat=10000)

    log.info(
        f"[test_cmp_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cmp_immediate(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cmp_immediate (CMP Immediate) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value

    bus.ram.data[0x1000] = 0x30  # Immediate value

    # First, test functionality:
    arithmetic.cmp_immediate()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 2, "CMP Immediate instruction should take 2 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cmp_immediate, repeat=10000)

    log.info(
        f"[test_cmp_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cmp_absolute(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cmp_absolute (CMP Absolute) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value

    bus.ram.data[0x1000] = 0x34  # Low byte of address
    bus.ram.data[0x1001] = 0x12  # High byte of address
    address = (0x12 << 8) | 0x34
    bus.ram.data[address] = 0x30  # Value at the absolute address

    # First, test functionality:
    arithmetic.cmp_absolute()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 4, "CMP Absolute instruction should take 4 cycles"

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.cmp_absolute, repeat=10000)

    log.info(
        f"[test_cmp_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cmp_absolute_x(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cmp_absolute_x (CMP Absolute,X) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.x = 0x05  # X register offset

    bus.ram.data[0x1000] = 0x34  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    target_address = (base_address + 0x05) & 0xFFFF  # Applying X offset
    bus.ram.data[target_address] = 0x30  # Value at the target address

    # First, test functionality:
    arithmetic.cmp_absolute_x()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count, accounting for page crossing
    page_crossed = (base_address & 0xFF00) != (target_address & 0xFF00)
    expected_cycles = 4 + (1 if page_crossed else 0)
    assert bus.cpu.cycles == expected_cycles, (
        f"CMP Absolute,X instruction should take {expected_cycles} cycles"
    )

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.cmp_absolute_x, repeat=10000)

    log.info(
        f"[test_cmp_absolute_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_bit_absolute(bus, arithmetic, time_instruction) -> None:
    """
    Tests the bit_absolute (BIT Absolute) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value

    bus.ram.data[0x1000] = 0x34  # Low byte of address
    bus.ram.data[0x1001] = 0x12  # High byte of address
    address = (0x12 << 8) | 0x34
    bus.ram.data[address] = 0x30  # Value at the absolute address

    # First, test functionality:
    arithmetic.bit_absolute()

    expected_zero = (bus.cpu.a & 0x30) == 0
    expected_overflow = (0x30 & 0x40) != 0
    expected_negative = (0x30 & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 4, "BIT Absolute instruction should take 4 cycles"

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.bit_absolute, repeat=10000)

    log.info(
        f"[test_bit_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_bit_zero_page(bus, arithmetic, time_instruction) -> None:
    """
    Tests the bit_zero_page (BIT Zero Page) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x30  # Value at the zero-page address

    # First, test functionality:
    arithmetic.bit_zero_page()

    expected_zero = (bus.cpu.a & 0x30) == 0
    expected_overflow = (0x30 & 0x40) != 0
    expected_negative = (0x30 & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 3, "BIT Zero Page instruction should take 3 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.bit_zero_page, repeat=10000)

    log.info(
        f"[test_bit_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cpx_zero_page(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cpx_zero_page (CPX Zero Page) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x50  # Initial X register value

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x30  # Value at the zero-page address

    # First, test functionality:
    arithmetic.cpx_zero_page()

    expected_carry = 0x50 >= 0x30
    expected_zero = 0x50 == 0x30
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 3, "CPX Zero Page instruction should take 3 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cpx_zero_page, repeat=10000)

    log.info(
        f"[test_cpx_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cpx_immediate(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cpx_immediate (CPX Immediate) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x50  # Initial X register value

    bus.ram.data[0x1000] = 0x30  # Immediate value

    # First, test functionality:
    arithmetic.cpx_immediate()

    expected_carry = 0x50 >= 0x30
    expected_zero = (0x50 - 0x30) & 0xFF == 0
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 2, "CPX Immediate instruction should take 2 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cpx_immediate, repeat=10000)

    log.info(
        f"[test_cpx_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cpx_absolute(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cpx_absolute (CPX Absolute) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x50  # Initial X register value

    bus.ram.data[0x1000] = 0x34  # Low byte of address
    bus.ram.data[0x1001] = 0x12  # High byte of address
    address = (0x12 << 8) | 0x34
    bus.ram.data[address] = 0x30  # Value at the absolute address

    # First, test functionality:
    arithmetic.cpx_absolute()

    expected_carry = 0x50 >= 0x30
    expected_zero = (0x50 - 0x30) & 0xFF == 0
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 4, "CPX Absolute instruction should take 4 cycles"

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.cpx_absolute, repeat=10000)

    log.info(
        f"[test_cpx_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cpy_immediate(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cpy_immediate (CPY Immediate) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x50  # Initial Y register value

    bus.ram.data[0x1000] = 0x30  # Immediate value

    # First, test functionality:
    arithmetic.cpy_immediate()

    expected_carry = 0x50 >= 0x30
    expected_zero = (0x50 - 0x30) & 0xFF == 0
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 2, "CPY Immediate instruction should take 2 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cpy_immediate, repeat=10000)

    log.info(
        f"[test_cpy_immediate] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_cpy_zero_page(bus, arithmetic, time_instruction) -> None:
    """
    Tests the cpy_zero_page (CPY Zero Page) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.y = 0x50  # Initial Y register value

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x30  # Value at the zero-page address

    # First, test functionality:
    arithmetic.cpy_zero_page()

    expected_carry = 0x50 >= 0x30
    expected_zero = (0x50 - 0x30) & 0xFF == 0
    expected_negative = ((0x50 - 0x30) & 0x80) != 0

    # Check flags
    assert (bus.cpu.status & 0x01) == (0x01 if expected_carry else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (0x02 if expected_zero else 0x00), (
        "Zero flag incorrect"
    )
    assert (bus.cpu.status & 0x80) == (0x80 if expected_negative else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 3, "CPY Zero Page instruction should take 3 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.cpy_zero_page, repeat=10000)

    log.info(
        f"[test_cpy_zero_page] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_adc_immediate_binary(bus, arithmetic, time_instruction) -> None:
    """Tests the adc_immediate (ADC Immediate) instruction in binary mode."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.status &= ~0x08  # Clear Decimal Mode flag (D)
    bus.cpu.status |= 0x01  # Set Carry flag (C)

    bus.ram.data[0x1000] = 0x30  # Immediate value

    # First, test functionality:
    arithmetic.adc_immediate()

    expected_result = 0x50 + 0x30 + 1  # A + Immediate + Carry
    expected_carry = expected_result > 0xFF
    expected_zero = (expected_result & 0xFF) == 0
    expected_negative = (expected_result & 0x80) != 0
    expected_overflow = (((0x50 ^ 0x30) & 0x80) == 0) and (
        ((0x50 ^ expected_result) & 0x80) != 0
    )

    # Check results
    assert bus.cpu.a == (expected_result & 0xFF), (
        f"A should be {hex(expected_result & 0xFF)}, but got {hex(bus.cpu.a)}"
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
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 2, "ADC Immediate instruction should take 2 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.adc_immediate, repeat=10000)

    log.info(
        f"[test_adc_immediate_binary] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_adc_immediate_bcd(bus, arithmetic, time_instruction) -> None:
    """Tests the adc_immediate (ADC Immediate) instruction in BCD mode."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x25  # Initial A register value
    bus.cpu.status |= 0x08  # Set Decimal Mode flag (D)
    bus.cpu.status |= 0x01  # Set Carry flag (C)

    bus.ram.data[0x1000] = 0x37  # Immediate value

    # First, test functionality:
    arithmetic.adc_immediate()

    # BCD Calculation
    temp = (0x25 & 0x0F) + (0x37 & 0x0F) + 1
    carry_nibble = 1 if temp > 9 else 0
    if temp > 9:
        temp += 6

    temp2 = (0x25 & 0xF0) + (0x37 & 0xF0) + (carry_nibble << 4)
    carry_out = 1 if temp2 > 0x90 else 0
    if temp2 > 0x90:
        temp2 += 0x60

    expected_result = (temp & 0x0F) | (temp2 & 0xF0)

    # Check results
    assert bus.cpu.a == (expected_result & 0xFF), (
        f"A should be {hex(expected_result & 0xFF)}, but got {hex(bus.cpu.a)}"
    )
    assert (bus.cpu.status & 0x01) == (0x01 if carry_out else 0x00), (
        "Carry flag incorrect"
    )
    assert (bus.cpu.status & 0x02) == (
        0x02 if (expected_result & 0xFF) == 0 else 0x00
    ), "Zero flag incorrect"
    assert (bus.cpu.status & 0x80) == (0x80 if (expected_result & 0x80) else 0x00), (
        "Negative flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 2, "ADC Immediate instruction should take 2 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.adc_immediate, repeat=10000)

    log.info(
        f"[test_adc_immediate_bcd] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_adc_zero_page_no_overflow(bus, arithmetic, time_instruction) -> None:
    """Tests the adc_zero_page (ADC Zero Page) instruction without overflow."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x20  # Initial A register value
    bus.cpu.status |= 0x01  # Set Carry flag (C)

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x10  # Value at the zero-page address

    # First, test functionality:
    arithmetic.adc_zero_page()

    expected_result = 0x20 + 0x10 + 1  # A + Memory + Carry
    expected_carry = expected_result > 0xFF
    expected_zero = (expected_result & 0xFF) == 0
    expected_negative = (expected_result & 0x80) != 0
    expected_overflow = (~(0x20 ^ 0x10) & (0x20 ^ expected_result) & 0x80) != 0

    # Check results
    assert bus.cpu.a == (expected_result & 0xFF), (
        f"A should be {hex(expected_result & 0xFF)}, but got {hex(bus.cpu.a)}"
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
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 3, "ADC Zero Page instruction should take 3 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.adc_zero_page, repeat=10000)

    log.info(
        f"[test_adc_zero_page_no_overflow] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_adc_zero_page_overflow(bus, arithmetic, time_instruction) -> None:
    """Tests the adc_zero_page (ADC Zero Page) instruction with overflow."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x7F  # Initial A register value (near max positive)
    bus.cpu.status &= ~0x01  # Clear Carry flag (C)

    bus.ram.data[0x1000] = 0x80  # Zero-page address
    bus.ram.data[0x80] = 0x02  # Value at the zero-page address

    # First, test functionality:
    arithmetic.adc_zero_page()

    expected_result = 0x7F + 0x02 + 0  # A + Memory + Carry
    expected_carry = expected_result > 0xFF
    expected_zero = (expected_result & 0xFF) == 0
    expected_negative = (expected_result & 0x80) != 0
    expected_overflow = (~(0x7F ^ 0x02) & (0x7F ^ expected_result) & 0x80) != 0

    # Check results
    assert bus.cpu.a == (expected_result & 0xFF), (
        f"A should be {hex(expected_result & 0xFF)}, but got {hex(bus.cpu.a)}"
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
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )

    # Check cycle count
    assert bus.cpu.cycles == 3, "ADC Zero Page instruction should take 3 cycles"

    assert bus.cpu.pc == 0x1001, "PC should have incremented by 1"

    total_time, avg_time = time_instruction(arithmetic.adc_zero_page, repeat=10000)

    log.info(
        f"[test_adc_zero_page_overflow] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_adc_absolute_y_no_page_cross(bus, arithmetic, time_instruction) -> None:
    """Tests the adc_absolute_y (ADC Absolute,Y) instruction without page crossing."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x20  # Initial A register value
    bus.cpu.y = 0x05  # Y register offset
    bus.cpu.status |= 0x01  # Set Carry flag (C)

    bus.ram.data[0x1000] = 0x34  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0x34
    effective_address = (base_address + 0x05) & 0xFFFF  # Applying Y offset
    bus.ram.data[effective_address] = 0x10  # Value at the effective address

    # First, test functionality:
    arithmetic.adc_absolute_y()

    expected_result = 0x20 + 0x10 + 1  # A + Memory + Carry
    expected_carry = expected_result > 0xFF
    expected_zero = (expected_result & 0xFF) == 0
    expected_negative = (expected_result & 0x80) != 0
    expected_overflow = (~(0x20 ^ 0x10) & (0x20 ^ expected_result) & 0x80) != 0

    # Check results
    assert bus.cpu.a == (expected_result & 0xFF), (
        f"A should be {hex(expected_result & 0xFF)}, but got {hex(bus.cpu.a)}"
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
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )

    # Check cycle count (no page crossing)
    assert bus.cpu.cycles == 4, "ADC Absolute,Y instruction should take 4 cycles"

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.adc_absolute_y, repeat=10000)

    log.info(
        f"[test_adc_absolute_y_no_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_adc_absolute_y_page_cross(bus, arithmetic, time_instruction) -> None:
    """Tests the adc_absolute_y (ADC Absolute,Y) instruction with page crossing."""
    bus.cpu.pc = 0x1000
    bus.cpu.a = 0x50  # Initial A register value
    bus.cpu.y = 0xF0  # Y register offset (causing page crossing)
    bus.cpu.status &= ~0x01  # Clear Carry flag (C)

    bus.ram.data[0x1000] = 0xFF  # Low byte of base address
    bus.ram.data[0x1001] = 0x12  # High byte of base address
    base_address = (0x12 << 8) | 0xFF
    effective_address = (base_address + 0xF0) & 0xFFFF  # Applying Y offset
    bus.ram.data[effective_address] = 0x30  # Value at the effective address

    # First, test functionality:
    arithmetic.adc_absolute_y()

    expected_result = 0x50 + 0x30 + 0  # A + Memory + Carry
    expected_carry = expected_result > 0xFF
    expected_zero = (expected_result & 0xFF) == 0
    expected_negative = (expected_result & 0x80) != 0
    expected_overflow = (~(0x50 ^ 0x30) & (0x50 ^ expected_result) & 0x80) != 0

    # Check results
    assert bus.cpu.a == (expected_result & 0xFF), (
        f"A should be {hex(expected_result & 0xFF)}, but got {hex(bus.cpu.a)}"
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
    assert (bus.cpu.status & 0x40) == (0x40 if expected_overflow else 0x00), (
        "Overflow flag incorrect"
    )

    # Check cycle count (extra cycle for page crossing)
    assert bus.cpu.cycles == 5, (
        "ADC Absolute,Y instruction should take 5 cycles due to page crossing"
    )

    assert bus.cpu.pc == 0x1002, "PC should have incremented by 2"

    total_time, avg_time = time_instruction(arithmetic.adc_absolute_y, repeat=10000)

    log.info(
        f"[test_adc_absolute_y_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )
