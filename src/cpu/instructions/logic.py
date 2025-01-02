from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Logic:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def and_indirect_y(self) -> None:
        zp_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        base_address = self.cpu.read_word_le(zp_address)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.a &= self.cpu.read_memory_int(effective_address)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 5

    def and_immediate(self) -> None:
        self.cpu.a &= self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def and_zero_page(self) -> None:
        self.cpu.a &= self.cpu.read_memory_int(self.cpu.read_memory_int(self.cpu.pc))
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 3

    def asl_accumulator(self) -> None:
        self.cpu.status = (self.cpu.status & ~0x01) | (
            (self.cpu.a >> 7) & 0x01
        )  # Update Carry flag
        self.cpu.a = (self.cpu.a << 1) & 0xFF  # Shift left, keep within 8-bit range
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def asl_zero_page(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address)
        self.cpu.status = (self.cpu.status & ~0x01) | (
            (value >> 7) & 0x01
        )  # Update Carry flag
        result = (value << 1) & 0xFF
        self.cpu.bus.write(zero_page_address, result)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if result == 0 else 0)
            | (0x80 if result & 0x80 else 0)
        )
        self.cpu.cycles += 5

    def asl_zero_page_x(self) -> None:
        zero_page_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address)
        self.cpu.status = (self.cpu.status & ~0x01) | (
            (value >> 7) & 0x01
        )  # Update Carry flag
        result = (value << 1) & 0xFF
        self.cpu.bus.write(zero_page_address, result)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if result == 0 else 0)
            | (0x80 if result & 0x80 else 0)
        )
        self.cpu.cycles += 6

    def eor_zero_page_x(self) -> None:
        effective_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        self.cpu.a ^= self.cpu.read_memory_int(effective_address)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 4

    def eor_immediate(self) -> None:
        self.cpu.a ^= self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def eor_indirect_x(self) -> None:
        base_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        target_address = (
            self.cpu.read_memory_int((base_address + 1) & 0xFF) << 8
        ) | self.cpu.read_memory_int(base_address)
        self.cpu.a ^= self.cpu.read_memory_int(target_address)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 6

    def eor_zero_page(self) -> None:
        self.cpu.a ^= self.cpu.read_memory_int(self.cpu.read_memory_int(self.cpu.pc))
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 3

    def lsr_accumulator(self) -> None:
        self.cpu.status = (self.cpu.status & ~0x01) | (
            self.cpu.a & 0x01
        )  # Set Carry flag if bit 0 is 1
        self.cpu.a = (self.cpu.a >> 1) & 0xFF  # Shift right, keeping within 8-bit range
        self.cpu.status = (self.cpu.status & ~0x82) | (0x02 if self.cpu.a == 0 else 0)
        self.cpu.cycles += 2

    def lsr_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        self.cpu.status = (self.cpu.status & ~0x01) | (
            value & 0x01
        )  # Set Carry flag if bit 0 is 1
        result = (value >> 1) & 0xFF
        self.cpu.bus.write(address, result)
        self.cpu.status = (self.cpu.status & ~0x82) | (0x02 if result == 0 else 0)
        self.cpu.cycles += 5

    def lsr_zero_page_x(self) -> None:
        address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        self.cpu.status = (self.cpu.status & ~0x01) | (value & 0x01)
        result = value >> 1
        self.cpu.bus.write(address, result)
        self.cpu.status = (self.cpu.status & ~0x82) | (0x02 if result == 0 else 0)
        self.cpu.cycles += 6

    def ora_zero_page(self) -> None:
        self.cpu.a |= self.cpu.read_memory_int(self.cpu.read_memory_int(self.cpu.pc))
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 3

    def ora_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        self.cpu.a |= self.cpu.read_memory_int(address)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 4

    def ora_immediate(self) -> None:
        self.cpu.a |= self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def ora_indirect_indexed(self) -> None:
        zp_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        base_address = self.cpu.read_word_le(zp_address)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.a |= self.cpu.read_memory_int(effective_address)
        self.cpu.status = (
            (self.cpu.status & ~0x82)
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 5 + (
            1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
        )

    def rol_accumulator(self) -> None:
        carry_in = self.cpu.status & 0x01  # Extract Carry flag (bit 0)
        new_carry = (self.cpu.a & 0x80) >> 7  # Extract bit 7 as new Carry
        self.cpu.a = ((self.cpu.a << 1) | carry_in) & 0xFF  # Rotate left with Carry-in
        self.cpu.status = (
            (self.cpu.status & ~0x83)
            | new_carry
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def rol_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        carry_in = self.cpu.status & 0x01  # Extract Carry flag (bit 0)
        new_carry = (value & 0x80) >> 7  # Extract bit 7 as new Carry
        result = ((value << 1) | carry_in) & 0xFF  # Rotate left with Carry-in
        self.cpu.bus.write(address, result)
        self.cpu.status = (
            (self.cpu.status & ~0x83)
            | new_carry
            | (0x02 if result == 0 else 0)
            | (0x80 if result & 0x80 else 0)
        )
        self.cpu.cycles += 5

    def ror_accumulator(self) -> None:
        carry_in = self.cpu.status & 0x01  # Extract Carry flag (bit 0)
        new_carry = self.cpu.a & 0x01  # Extract bit 0 as new Carry
        self.cpu.a = (
            (self.cpu.a >> 1) | (carry_in << 7)
        ) & 0xFF  # Rotate right with Carry-in
        self.cpu.status = (
            (self.cpu.status & ~0x83)
            | new_carry
            | (0x02 if self.cpu.a == 0 else 0)
            | (0x80 if self.cpu.a & 0x80 else 0)
        )
        self.cpu.cycles += 2

    def ror_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        carry_in = self.cpu.status & 0x01  # Extract Carry flag (bit 0)
        new_carry = value & 0x01  # Extract bit 0 as new Carry
        result = ((value >> 1) | (carry_in << 7)) & 0xFF  # Rotate right with Carry-in
        self.cpu.bus.write(address, result)
        self.cpu.status = (
            (self.cpu.status & ~0x83)
            | new_carry
            | (0x02 if result == 0 else 0)
            | (0x80 if result & 0x80 else 0)
        )
        self.cpu.cycles += 5

    def ror_zero_page_x(self) -> None:
        address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        carry_in = self.cpu.status & 0x01  # Extract Carry flag (bit 0)
        new_carry = value & 0x01  # Extract bit 0 as new Carry
        result = ((value >> 1) | (carry_in << 7)) & 0xFF  # Rotate right with Carry-in
        self.cpu.bus.write(address, result)
        self.cpu.status = (
            (self.cpu.status & ~0x83)
            | new_carry
            | (0x02 if result == 0 else 0)
            | (0x80 if result & 0x80 else 0)
        )
        self.cpu.cycles += 6

    def ror_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        value = self.cpu.read_memory_int(address)
        carry_in = self.cpu.status & 0x01  # Extract Carry flag (bit 0)
        new_carry = value & 0x01  # Extract bit 0 as new Carry
        result = ((value >> 1) | (carry_in << 7)) & 0xFF  # Rotate right with Carry-in
        self.cpu.bus.write(address, result)
        self.cpu.status = (
            (self.cpu.status & ~0x83)
            | new_carry
            | (0x02 if result == 0 else 0)
            | (0x80 if result & 0x80 else 0)
        )
        self.cpu.cycles += 6
