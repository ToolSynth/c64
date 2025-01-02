from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Branch:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def beq(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        signed_offset = offset if offset < 0x80 else offset - 256
        if self.cpu.status & 0x02:  # Check if Z flag is set (bit 1)
            new_pc = (self.cpu.pc + signed_offset) & 0xFFFF
            self.cpu.cycles += 1 if (self.cpu.pc & 0xFF00) != (new_pc & 0xFF00) else 0
            self.cpu.pc = new_pc
            self.cpu.cycles += 1  # Extra cycle for branching
        self.cpu.cycles += 2  # Base cycles

    def bne(self) -> None:
        """BNE - Branch if Not Equal (Z = 0)"""
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        signed_offset = offset if offset < 0x80 else offset - 256
        self.cpu.cycles += 2  # Base cycles
        if not (self.cpu.status & 0x02):  # Check if Z flag is clear (Zero flag not set)
            old_pc = self.cpu.pc  # Store the old PC before branching
            self.cpu.pc = (self.cpu.pc + signed_offset) & 0xFFFF  # Apply branch offset

            self.cpu.cycles += 1  # Extra cycle for taking the branch

            # Extra cycle only if the branch crosses a page
            if (old_pc & 0xFF00) != (self.cpu.pc & 0xFF00):
                self.cpu.cycles += 1

    def bpl(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        signed_offset = offset if offset < 0x80 else offset - 256
        if not (self.cpu.status & 0x80):  # Check if N flag is clear
            new_pc = (self.cpu.pc + signed_offset) & 0xFFFF
            self.cpu.cycles += 1 if (self.cpu.pc & 0xFF00) != (new_pc & 0xFF00) else 0
            self.cpu.pc = new_pc
            self.cpu.cycles += 1  # Extra cycle for branching
        self.cpu.cycles += 2  # Base cycles

    def bmi(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        signed_offset = offset if offset < 0x80 else offset - 256
        if self.cpu.status & 0x80:  # Check if N flag is set (bit 7)
            new_pc = (self.cpu.pc + signed_offset) & 0xFFFF
            self.cpu.cycles += 1 if (self.cpu.pc & 0xFF00) != (new_pc & 0xFF00) else 0
            self.cpu.pc = new_pc
            self.cpu.cycles += 1  # Extra cycle for branching
        self.cpu.cycles += 2  # Base cycles

    def bvs(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        signed_offset = offset if offset < 0x80 else offset - 256

        self.cpu.cycles += 2  # Base cycles

        if self.cpu.status & 0x40:  # Check if V flag is set (bit 6)
            old_pc = self.cpu.pc  # Store the old PC before branching
            self.cpu.pc = (self.cpu.pc + signed_offset) & 0xFFFF  # Apply branch offset

            self.cpu.cycles += 1  # Extra cycle for taking the branch

            # Extra cycle only if the branch crosses a page
            if (old_pc & 0xFF00) != (self.cpu.pc & 0xFF00):
                self.cpu.cycles += 1

    def bcc(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        signed_offset = offset if offset < 0x80 else offset - 256
        if not (self.cpu.status & 0x01):  # Check if C flag is clear (bit 0)
            new_pc = (self.cpu.pc + signed_offset) & 0xFFFF
            self.cpu.cycles += 1 if (self.cpu.pc & 0xFF00) != (new_pc & 0xFF00) else 0
            self.cpu.pc = new_pc
            self.cpu.cycles += 1  # Extra cycle for branching
        self.cpu.cycles += 2  # Base cycles

    def bcs(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.cycles += 2  # Base cycles
        if self.cpu.status & 0x01:  # Check if Carry flag is set (bit 0)
            old_pc = self.cpu.pc
            self.cpu.pc = (
                old_pc + (offset if offset < 0x80 else offset - 256)
            ) & 0xFFFF
            self.cpu.cycles += 1  # Extra cycle for taking the branch
            self.cpu.cycles += 1 if (old_pc & 0xFF00) != (self.cpu.pc & 0xFF00) else 0

    def bvc(self) -> None:
        offset = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.cycles += 2  # Base cycles
        if not (self.cpu.status & 0x40):  # Check if Overflow flag is clear (bit 6)
            old_pc = self.cpu.pc
            self.cpu.pc = (
                old_pc + (offset if offset < 0x80 else offset - 256)
            ) & 0xFFFF
            self.cpu.cycles += 1  # Extra cycle for taking the branch
            self.cpu.cycles += 1 if (old_pc & 0xFF00) != (self.cpu.pc & 0xFF00) else 0
