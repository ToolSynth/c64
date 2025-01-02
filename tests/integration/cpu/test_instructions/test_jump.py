import pytest

from src.cpu.instructions.jump import Jump
from src.utils.log_setup import log


@pytest.fixture()
def jump(bus):
    return Jump(bus.cpu)


def test_jmp_indirect_x(bus, jump, time_instruction):
    """
    Tests the jmp_indirect_x (JMP (Indirect, X)) instruction
    and measures its execution time.
    """
    bus.cpu.pc = 0x1000
    bus.cpu.x = 0x02
    bus.ram.data[0x1000] = 0x00  # low byte of the base address
    bus.ram.data[0x1001] = 0x20  # high byte of the base address
    bus.ram.data[0x2002] = 0x34  # low target
    bus.ram.data[0x2003] = 0x12  # high target

    # First, test functionality:
    jump.jmp_indirect_x()
    assert bus.cpu.pc == 0x1234, (
        "PC should point to 0x1234 after JMP (Indirect, X) jump"
    )
    assert bus.cpu.cycles == 5, "JMP (Indirect, X) instruction should take 5 cycles"

    total_time, avg_time = time_instruction(jump.jmp_indirect_x, repeat=10000)

    log.info(
        f"[test_jmp_indirect_x] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_jmp_absolute(bus, jump, time_instruction):
    """
    Tests the jmp_absolute (JMP Absolute) instruction.
    - At PC=0x0000, we set the target_address = 0xABCD (low=0xCD, high=0xAB)
    - We expect PC to point to 0xABCD at the end
    - Check the cycle increment = +3
    """
    bus.cpu.pc = 0x0000
    bus.ram.data[0x0000] = 0xCD  # low
    bus.ram.data[0x0001] = 0xAB  # high

    jump.jmp_absolute()

    assert bus.cpu.pc == 0xABCD, "PC should point to 0xABCD after JMP Absolute"
    assert bus.cpu.cycles == 3, "JMP Absolute instruction should take 3 cycles"

    total_time, avg_time = time_instruction(jump.jmp_indirect_x, repeat=10000)

    log.info(
        f"[test_jmp_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_jmp_indirect_normal(bus, jump, time_instruction):
    """
    Tests the jmp_indirect (JMP (Absolute)) instruction.
    - At PC=0x1000, we set a pointer (0x3000) => low=0x00, high=0x30
    - At 0x3000 and 0x3001, we store the target address 0x5678 (low=0x78, high=0x56)
    - We expect the jump to occur at 0x5678
    - Check the cycle increment = +5
    """
    bus.cpu.pc = 0x1000
    bus.ram.data[0x1000] = 0x00  # pointer low
    bus.ram.data[0x1001] = 0x30  # pointer high
    bus.ram.data[0x3000] = 0x78  # target low
    bus.ram.data[0x3001] = 0x56  # target high

    jump.jmp_indirect()

    assert bus.cpu.pc == 0x5678, "PC should point to 0x5678 after JMP Indirect"
    assert bus.cpu.cycles == 5, "JMP Indirect instruction should take 5 cycles"

    total_time, avg_time = time_instruction(jump.jmp_indirect, repeat=10000)

    log.info(
        f"[test_jmp_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_jmp_indirect_page_boundary_bug(bus, jump):
    """
    Tests the 'Page boundary bug' in the jmp_indirect instruction:
    - If the pointer is at the end of a page (e.g., 0x30FF), the high byte
      is fetched from 0x3000 (instead of 0x3100) according to the 6502 processor bug.
    - We set the pointer = 0x30FF and store the target address at 0x30FF and 0x3000.
    """
    bus.cpu.pc = 0x2000
    # Store the pointer = 0x30FF
    bus.ram.data[0x2000] = 0xFF  # low
    bus.ram.data[0x2001] = 0x30  # high

    # Store the target address:
    #   * low (at 0x30FF) = 0xAA
    #   * high (at 0x3000, not 0x3100) = 0xBB
    # Thus, the target address is 0xBBAA
    bus.ram.data[0x30FF] = 0xAA
    bus.ram.data[0x3000] = 0xBB

    jump.jmp_indirect()
    assert bus.cpu.pc == 0xBBAA, (
        "PC should point to 0xBBAA (page boundary bug) after JMP Indirect"
    )


def test_jsr(bus, jump, time_instruction):
    """
    Tests the jsr (Jump to SubRoutine) instruction.
    - At PC=0x1000, we set the target address 0x3000 (low=0x00, high=0x30)
    - We expect:
       * PC to point to 0x3000
       * (PC+1) -> 0x1001 to be pushed onto the stack
       * SP to decrease by 2
    """
    bus.cpu.pc = 0x1000
    bus.ram.data[0x1000] = 0x00  # low
    bus.ram.data[0x1001] = 0x30  # high

    jump.jsr()

    assert bus.cpu.pc == 0x3000, "PC should point to 0x3000 after JSR"
    assert bus.cpu.sp == 0xFD, "Stack pointer should decrease by 2 (from 0xFF to 0xFD)"
    assert bus.cpu.cycles == 6, "JSR instruction should take 6 cycles"

    total_time, avg_time = time_instruction(jump.jmp_indirect_x, repeat=10000)

    log.info(
        f"[test_jmp_absolute] Repeated 10,000 times. "
        f"Total time: {total_time:.6f}s, Average: {avg_time:.9f}s"
    )


def test_rts_stack_underflow(bus, jump):
    """
    Tests stack underflow error when executing RTS,
    when sp = 0xFF (stack is empty). An exception is expected.
    """
    bus.cpu.sp = 0xFF  # Stack is empty

    with pytest.raises(Exception, match="Stack underflow"):
        jump.rts()


def test_rti(bus, jump):
    """
    Tests the rti (Return from Interrupt) instruction.
    - RTI restores the status register (P) and PC from three bytes on the stack.
      Order of retrieval: status, PC low, PC high.
    - Assume sp=0xFC, and at 0x01FD, 0x01FE, 0x01FF we have [status, pcl, pch].
    """
    bus.cpu.sp = 0xFC
    bus.ram.data[0x01FD] = 0b10101010  # example status
    bus.ram.data[0x01FE] = 0x34  # PC low
    bus.ram.data[0x01FF] = 0x12  # PC high

    jump.rti()

    assert bus.cpu.status == 0b10101010, "Status should be restored from stack"
    assert bus.cpu.pc == 0x1234, "PC should be restored from stack to 0x1234"
    assert bus.cpu.cycles == 6, "RTI instruction should take 6 cycles"
    assert bus.cpu.sp == 0xFF, "SP should increase by 3 (from 0xFC to 0xFF)"
