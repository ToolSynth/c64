from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Flag:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def clc(self) -> None:
        self.cpu.status &= ~0x01  # Clear Carry flag (bit 0)
        self.cpu.cycles += 2

    def cld(self) -> None:
        self.cpu.status &= ~0x08  # Clear Decimal Mode flag (bit 3)
        self.cpu.cycles += 2

    def sei(self) -> None:
        self.cpu.status |= 0x04  # Set Interrupt flag (bit 2)
        self.cpu.cycles += 2

    def cli(self) -> None:
        self.cpu.status &= ~0x04  # Clear Interrupt Disable flag (bit 2)

    def sec(self) -> None:
        self.cpu.status |= 0x01  # Set Carry flag (bit 0)
        self.cpu.cycles += 2
