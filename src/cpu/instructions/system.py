from __future__ import annotations

from typing import TYPE_CHECKING

from src.utils.log_setup import log

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class System:
    def __init__(self, cpu: CPU) -> None:
        self.cpu: CPU = cpu

    def brk(self, *, ignore_irq: bool = False) -> None:
        if ignore_irq:
            self.cpu.pc = (self.cpu.pc + 1) & 0xFFFF  # Skip BRK instruction
            return

        # BRK behaves like a two-byte instruction. Skip the padding byte so the
        # pushed PC points to the following instruction. The interrupt flag is
        # set before pushing the status so that the stored value reflects it.
        self.cpu.pc = (self.cpu.pc + 1) & 0xFFFF
        self.cpu.status |= 0x04  # Set interrupt-disable flag

        self.cpu.push((self.cpu.pc >> 8) & 0xFF)  # High byte of PC
        self.cpu.push(self.cpu.pc & 0xFF)  # Low byte of PC
        self.cpu.push(self.cpu.status | 0x10)  # Break flag set in copy

        self.cpu.pc = (
            self.cpu.read_memory_int(0xFFFF) << 8
        ) | self.cpu.read_memory_int(0xFFFE)
        self.cpu.cycles += 7

    def nop(self) -> None:
        """NOP - No Operation."""
        log.debug("NOP executed.")
        self.cpu.cycles += 2
