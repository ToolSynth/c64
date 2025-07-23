from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Stack:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def pha(self) -> None:
        self.cpu.bus.write(0x0100 + self.cpu.sp, self.cpu.a)
        self.cpu.sp = (self.cpu.sp - 1) & 0xFF
        self.cpu.cycles += 3

    def pla(self) -> None:
        self.cpu.sp = (self.cpu.sp + 1) & 0xFF
        self.cpu.a = self.cpu.read_memory_int(0x0100 + self.cpu.sp)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 4

    def txs(self) -> None:
        self.cpu.sp = self.cpu.x
        self.cpu.cycles += 2

    def php(self) -> None:
        self.cpu.bus.write(
            0x0100 + self.cpu.sp, self.cpu.status | 0x30
        )  # Force bits 4 and 5
        self.cpu.sp = (self.cpu.sp - 1) & 0xFF
        self.cpu.cycles += 3

    def plp(self) -> None:
        self.cpu.sp = (self.cpu.sp + 1) & 0xFF
        self.cpu.status = (
            self.cpu.read_memory_int(0x0100 + self.cpu.sp) & 0xEF
        ) | 0x20  # Masking out bit 4, forcing bit 5
        self.cpu.cycles += 4

    def tsx(self) -> None:
        self.cpu.x = self.cpu.sp
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.x == 0 else 0)
            | (0x80 if self.cpu.x & 0x80 else 0)
        )
        self.cpu.cycles += 2
