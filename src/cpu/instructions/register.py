from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Register:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def tax(self) -> None:
        self.cpu.x = self.cpu.a
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.x == 0 else 0)
            | (0x80 if self.cpu.x & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def tay(self) -> None:
        self.cpu.y = self.cpu.a
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.y == 0 else 0)
            | (0x80 if self.cpu.y & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def txa(self) -> None:
        self.cpu.a = self.cpu.x
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def tya(self) -> None:
        self.cpu.a = self.cpu.y
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def dex(self) -> None:
        self.cpu.x = (self.cpu.x - 1) & 0xFF
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.x == 0 else 0)
            | (0x80 if self.cpu.x & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def dey(self) -> None:
        self.cpu.y = (self.cpu.y - 1) & 0xFF
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.y == 0 else 0)
            | (0x80 if self.cpu.y & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def inx(self) -> None:
        self.cpu.x = (self.cpu.x + 1) & 0xFF
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.x == 0 else 0)
            | (0x80 if self.cpu.x & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def iny(self) -> None:
        self.cpu.y = (self.cpu.y + 1) & 0xFF
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.y == 0 else 0)
            | (0x80 if self.cpu.y & 0x80 else 0)
        )
        self.cpu.cycles += 2
