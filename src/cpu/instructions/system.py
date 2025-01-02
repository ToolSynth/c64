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
            self.cpu.pc += 1  # Skip BRK instruction
            return

        self.cpu.push((self.cpu.pc >> 8) & 0xFF)  # High byte of PC
        self.cpu.push(self.cpu.pc & 0xFF)  # Low byte of PC
        self.cpu.push(self.cpu.status | 0x10)  # Set Break flag in status
        self.cpu.status |= 0x04
        self.cpu.pc = (
            self.cpu.read_memory_int(0xFFFF) << 8
        ) | self.cpu.read_memory_int(0xFFFE)
        self.cpu.cycles += 7

    def nop(self) -> None:
        """NOP - No Operation."""
        log.debug("NOP executed.")
        self.cpu.cycles += 2
