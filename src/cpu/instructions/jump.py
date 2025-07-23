from typing import TYPE_CHECKING

from src.utils.log_setup import log

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class StackUnderflowError(RuntimeError):
    pass


class Jump:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def jmp_indirect_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        effective_address = base_address + self.cpu.x
        self.cpu.pc = self.cpu.read_word_le(effective_address)
        self.cpu.cycles += 5

    def jmp_absolute(self) -> None:
        self.cpu.pc = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.cycles += 3

    def jmp_indirect(self) -> None:
        indirect_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        if indirect_address < 0x0000 or indirect_address > 0xFFFF:
            log.error(
                f"Indirect address {indirect_address:#04X} is out of memory range!"
            )
            raise ValueError("Invalid indirect address!")

        if (indirect_address & 0xFF) == 0xFF:
            target_low = self.cpu.read_memory_int(indirect_address)
            target_high = self.cpu.read_memory_int(indirect_address & 0xFF00)
            log.debug(f"Page boundary bug triggered at address {hex(indirect_address)}")
        else:
            target_low = self.cpu.read_memory_int(indirect_address)
            target_high = self.cpu.read_memory_int((indirect_address + 1) & 0xFFFF)

        destination_address = (target_high << 8) | target_low
        self.cpu.pc = destination_address
        self.cpu.cycles += 5

    def jsr(self) -> None:
        target_address = self.cpu.read_word_le(self.cpu.pc)
        return_address = self.cpu.pc + 1
        stack_address_high = 0x0100 + self.cpu.sp
        self.cpu.bus.write(stack_address_high, (return_address >> 8) & 0xFF)
        self.cpu.sp -= 1
        stack_address_low = 0x0100 + self.cpu.sp
        self.cpu.bus.write(stack_address_low, return_address & 0xFF)
        self.cpu.sp -= 1
        self.cpu.pc = target_address
        self.cpu.cycles += 6

    def rts(self) -> None:
        if self.cpu.sp == 0xFF:
            raise StackUnderflowError("Stack underflow: RTS attempted with empty stack")

        low_address = 0x0100 + ((self.cpu.sp + 1) & 0xFF)
        high_address = 0x0100 + ((self.cpu.sp + 2) & 0xFF)
        low_byte = self.cpu.read_memory_int(low_address)
        high_byte = self.cpu.read_memory_int(high_address)
        return_address = (high_byte << 8) | low_byte
        self.cpu.sp = (self.cpu.sp + 2) & 0xFF
        self.cpu.pc = (return_address + 1) & 0xFFFF
        self.cpu.cycles += 6

    def rti(self) -> None:
        self.cpu.status = self.cpu.pull()
        pc_low = self.cpu.pull()
        pc_high = self.cpu.pull()
        self.cpu.pc = (pc_high << 8) | pc_low
        self.cpu.cycles += 6
