import pytest

from src.cpu.instructions.branch import Branch
from src.utils.log_setup import log


@pytest.fixture
def branch(bus):
    return Branch(bus.cpu)


def test_beq(bus, branch, time_instruction):
    """Tests the beq (Branch if Equal) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x02  # Set Z flag (Zero = 1)
    bus.ram.data[0x1000] = 0x10  # Offset +16

    # Execute instruction
    branch.beq()

    # Expected results
    expected_pc = 0x1011  # 0x1001 + 0x10
    expected_cycles = 3  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BEQ should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.beq, repeat=10000)

    log.info(
        f"[test_beq] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bne(bus, branch, time_instruction):
    """Tests the bne (Branch if Not Equal) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear Z flag (Zero = 0)
    bus.ram.data[0x1000] = 0xF0  # Offset -16 (negative offset)

    # Execute instruction
    branch.bne()

    # Expected results
    expected_pc = 0x0FF1
    expected_cycles = 4

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BNE should take 3 cycles when branching"


def test_bpl(bus, branch, time_instruction):
    """Tests the bpl (Branch if Positive) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear N flag (Negative = 0)
    bus.ram.data[0x1000] = 0x20  # Offset +32

    # Execute instruction
    branch.bpl()

    # Expected results
    expected_pc = 0x1021  # 0x1001 + 0x20
    expected_cycles = 3  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BPL should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bpl, repeat=10000)

    log.info(
        f"[test_bpl] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bpl_page_cross(bus, branch, time_instruction):
    """Tests the BPL instruction with a page crossing."""
    bus.cpu.pc = 0x10F0  # Near the page boundary
    bus.cpu.status = 0x00  # Clear N flag (Negative = 0)
    bus.ram.data[0x10F0] = 0x20  # Offset +32

    # Execute instruction
    branch.bpl()

    # Expected results
    expected_pc = 0x1111  # Crosses page from 0x10F1 to 0x1111
    expected_cycles = 4  # Base cycles + branch taken + page crossing

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, (
        "BPL should take 4 cycles when branching across pages"
    )

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bpl, repeat=10000)

    log.info(
        f"[test_bpl_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bmi(bus, branch, time_instruction):
    """Tests the bmi (Branch if Minus) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x80  # Set N flag (Negative = 1)
    bus.ram.data[0x1000] = 0x10  # Offset +16

    # Execute instruction
    branch.bmi()

    # Expected results
    expected_pc = 0x1011  # 0x1001 + 0x10
    expected_cycles = 3  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BMI should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bmi, repeat=10000)

    log.info(
        f"[test_bmi] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bvs(bus, branch, time_instruction):
    """Tests the bvs (Branch if Overflow Set) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x40  # Set V flag (Overflow = 1)
    bus.ram.data[0x1000] = 0xF0  # Offset -16 (negative offset)

    # Execute instruction
    branch.bvs()

    # Expected results
    expected_pc = 0x0FF1  # 0x1001 - 0x10
    expected_cycles = 4  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BVS should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bvs, repeat=10000)

    log.info(
        f"[test_bvs] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bcc(bus, branch, time_instruction):
    """Tests the bcc (Branch if Carry Clear) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear C flag (Carry = 0)
    bus.ram.data[0x1000] = 0x20  # Offset +32

    # Execute instruction
    branch.bcc()

    # Expected results
    expected_pc = 0x1021  # 0x1001 + 0x20
    expected_cycles = 3  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BCC should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bcc, repeat=10000)

    log.info(
        f"[test_bcc] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bcc_page_cross(bus, branch, time_instruction):
    """Tests the BCC instruction with a page crossing."""
    bus.cpu.pc = 0x10F0  # Near the page boundary
    bus.cpu.status = 0x00  # Clear C flag (Carry = 0)
    bus.ram.data[0x10F0] = 0x20  # Offset +32

    # Execute instruction
    branch.bcc()

    # Expected results
    expected_pc = 0x1111  # Crosses page from 0x10F1 to 0x1111
    expected_cycles = 4  # Base cycles + branch taken + page crossing

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, (
        "BCC should take 4 cycles when branching across pages"
    )

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bcc, repeat=10000)

    log.info(
        f"[test_bcc_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bcs(bus, branch, time_instruction):
    """Tests the BCS (Branch if Carry Set) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x01  # Set C flag (Carry = 1)
    bus.ram.data[0x1000] = 0x10  # Offset +16

    # Execute instruction
    branch.bcs()

    # Expected results
    expected_pc = 0x1011  # 0x1001 + 0x10
    expected_cycles = 3  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BCS should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bcs, repeat=10000)

    log.info(
        f"[test_bcs] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bcs_page_cross(bus, branch, time_instruction):
    """Tests the BCS instruction with a page crossing."""
    bus.cpu.pc = 0x10F0  # Near the page boundary
    bus.cpu.status = 0x01  # Set C flag (Carry = 1)
    bus.ram.data[0x10F0] = 0x20  # Offset +32

    # Execute instruction
    branch.bcs()

    # Expected results
    expected_pc = 0x1111  # Crosses page from 0x10F1 to 0x1111
    expected_cycles = 4  # Base cycles + branch taken + page crossing

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, (
        "BCS should take 4 cycles when branching across pages"
    )

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bcs, repeat=10000)

    log.info(
        f"[test_bcs_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bvc(bus, branch, time_instruction):
    """Tests the BVC (Branch if Overflow Clear) instruction."""
    bus.cpu.pc = 0x1000
    bus.cpu.status = 0x00  # Clear V flag (Overflow = 0)
    bus.ram.data[0x1000] = 0x10  # Offset +16

    # Execute instruction
    branch.bvc()

    # Expected results
    expected_pc = 0x1011  # 0x1001 + 0x10
    expected_cycles = 3  # Base cycles + branch taken

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, "BVC should take 3 cycles when branching"

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bvc, repeat=10000)

    log.info(
        f"[test_bvc] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )


def test_bvc_page_cross(bus, branch, time_instruction):
    """Tests the BVC instruction with a page crossing."""
    bus.cpu.pc = 0x10F0  # Near the page boundary
    bus.cpu.status = 0x00  # Clear V flag (Overflow = 0)
    bus.ram.data[0x10F0] = 0x20  # Offset +32

    # Execute instruction
    branch.bvc()

    # Expected results
    expected_pc = 0x1111  # Crosses page from 0x10F1 to 0x1111
    expected_cycles = 4  # Base cycles + branch taken + page crossing

    # Verify results
    assert bus.cpu.pc == expected_pc, (
        f"PC should be {hex(expected_pc)}, but got {hex(bus.cpu.pc)}"
    )
    assert bus.cpu.cycles == expected_cycles, (
        "BVC should take 4 cycles when branching across pages"
    )

    # Measure execution time
    total_time, avg_time = time_instruction(branch.bvc, repeat=10000)

    log.info(
        f"[test_bvc_page_cross] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average time: {avg_time:.9f}s"
    )
