from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Arithmetic:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def update_zero_and_negative_flags(self, value: int) -> None:
        value &= 0xFF
        self.cpu.status &= ~((1 << 1) | (1 << 7))  # Z=1, N=7
        if value == 0:
            self.cpu.status |= 1 << 1
        if value & 0x80:
            self.cpu.status |= 1 << 7

    def sbc_immediate(self) -> None:
        value = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        carry_in = self.cpu.status & 0x01  # Bit 0 = Carry flag
        decimal_mode = (self.cpu.status >> 3) & 1  # Bit 3 = Decimal flag

        if not decimal_mode:
            result = self.cpu.a - value - (1 - carry_in)
            self.cpu.status = (
                (self.cpu.status | 0x01) if result >= 0 else (self.cpu.status & ~0x01)
            )
            self.update_zero_and_negative_flags(result)

            # Ustawianie flagi V (Overflow)
            a_sign = self.cpu.a & 0x80
            m_sign = value & 0x80
            r_sign = result & 0x80
            overflow = ((a_sign ^ r_sign) & (a_sign ^ m_sign) & 0x80) != 0
            self.cpu.status = (
                (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
            )
            self.cpu.a = result & 0xFF
        else:
            raise NotImplementedError("Decimal")

        self.cpu.cycles += 2

    def sbc_absolute_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        effective_address = (base_address + self.cpu.x) & 0xFFFF
        memory_value = self.cpu.read_memory_int(effective_address)
        carry_flag = self.cpu.status & 0x01  # Bit 0 = Carry flag
        result = self.cpu.a - memory_value - (1 - carry_flag)
        self.update_zero_and_negative_flags(result & 0xFF)
        self.cpu.status = (
            (self.cpu.status | 0x01) if result >= 0 else (self.cpu.status & ~0x01)
        )
        self.cpu.a = result & 0xFF
        self.cpu.cycles += 4

    def sbc_absolute_y(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        value = self.cpu.read_memory_int(effective_address)
        carry_flag = self.cpu.status & 0x01  # Bit 0 = Carry flag
        result = self.cpu.a - value - (1 - carry_flag)
        self.update_zero_and_negative_flags(result & 0xFF)
        self.cpu.status = (
            (self.cpu.status | 0x01) if result >= 0 else (self.cpu.status & ~0x01)
        )
        overflow = ((self.cpu.a ^ result) & (self.cpu.a ^ value) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )
        self.cpu.a = result & 0xFF
        self.cpu.cycles += 4

    def sbc_zero_page(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address) ^ 0xFF
        carry = self.cpu.status & 0x01  # Bit 0 = Carry flag
        result = self.cpu.a + value + carry
        self.cpu.status = (
            (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
        )
        overflow = ((self.cpu.a ^ result) & (value ^ result) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )
        self.cpu.a = result & 0xFF
        self.update_zero_and_negative_flags(self.cpu.a)
        self.cpu.cycles += 3

    def sbc_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        value = self.cpu.read_memory_int(address) ^ 0xFF
        carry = 1 if (self.cpu.status & 0x01) else 0  # Bit 0 = Carry flag
        result = self.cpu.a + value + carry
        self.cpu.status = (
            (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        overflow = ((self.cpu.a ^ result) & (value ^ result) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )  # Overflow flag (Bit 6)
        self.cpu.a = result & 0xFF
        self.update_zero_and_negative_flags(self.cpu.a)
        self.cpu.cycles += 4

    def sbc_zero_page_x(self) -> None:
        zero_page_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address) ^ 0xFF
        carry = 1 if (self.cpu.status & 0x01) else 0  # Bit 0 = Carry flag
        result = self.cpu.a + value + carry
        self.cpu.status = (
            (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        overflow = ((self.cpu.a ^ result) & (value ^ result) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )  # Overflow flag (Bit 6)
        self.cpu.a = result & 0xFF  # Mask result to 8 bits
        self.update_zero_and_negative_flags(self.cpu.a)
        self.cpu.cycles += 4

    def sbc_indirect_y(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        base_address = self.cpu.read_word_le(zero_page_address)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        value = self.cpu.read_memory_int(effective_address) ^ 0xFF
        carry = 1 if (self.cpu.status & 0x01) else 0  # Bit 0 = Carry flag
        result = self.cpu.a + value + carry
        self.cpu.status = (
            (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        overflow = ((self.cpu.a ^ result) & (value ^ result) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )  # Overflow flag (Bit 6)
        self.cpu.a = result & 0xFF
        self.update_zero_and_negative_flags(self.cpu.a)
        # Page crossing check (adds extra cycle if crossed)
        page_crossed = (base_address & 0xFF00) != (effective_address & 0xFF00)
        self.cpu.cycles += 5 + (1 if page_crossed else 0)

    def cmp_indirect_y(self) -> None:
        zp_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        base_address = self.cpu.read_word_le(zp_address)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        page_crossed = (base_address & 0xFF00) != (effective_address & 0xFF00)
        self.cpu.cycles += 5 + (1 if page_crossed else 0)
        value = self.cpu.read_memory_int(effective_address)
        result = (self.cpu.a - value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.a >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02)
            if self.cpu.a == value
            else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)

    def cmp_absolute_y(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        target_address = (base_address + self.cpu.y) & 0xFFFF
        value = self.cpu.read_memory_int(target_address)
        result = (self.cpu.a - value) & 0xFF
        # Set flags directly in self.status
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.a >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02)
            if self.cpu.a == value
            else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        # Check if a page boundary was crossed
        page_crossed = (base_address & 0xFF00) != (target_address & 0xFF00)
        self.cpu.cycles += 4 + (1 if page_crossed else 0)

    def cmp_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        result = (self.cpu.a - value) & 0xFF
        # Set flags directly in self.status
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.a >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 3

    def cmp_immediate(self) -> None:
        value = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        result = (self.cpu.a - value) & 0xFF
        # Set flags directly in self.status
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.a >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 2

    def cmp_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        value = self.cpu.read_memory_int(address)
        result = (self.cpu.a - value) & 0xFF
        # Set flags directly in self.cpu.status
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.a >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 4

    def cmp_absolute_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        target_address = (base_address + self.cpu.x) & 0xFFFF
        page_crossed = (base_address & 0xFF00) != (target_address & 0xFF00)
        self.cpu.cycles += 4 + (1 if page_crossed else 0)
        value = self.cpu.read_memory_int(target_address)
        result = (self.cpu.a - value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.a >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)

    def bit_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        value = self.cpu.read_memory_int(address)
        result = self.cpu.a & value
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x40) if (value & 0x40) else (self.cpu.status & ~0x40)
        )  # Overflow flag (Bit 6)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (value & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.pc += 2
        self.cpu.cycles += 4

    def bit_zero_page(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address)
        result = self.cpu.a & value
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x40) if (value & 0x40) else (self.cpu.status & ~0x40)
        )  # Overflow flag (Bit 6)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (value & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 3

    def cpx_zero_page(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        memory_value = self.cpu.read_memory_int(zero_page_address)
        result = (self.cpu.x - memory_value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.x >= memory_value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 3

    def cpx_immediate(self) -> None:
        value = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        result = (self.cpu.x - value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.x >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 2

    def cpx_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        value = self.cpu.read_memory_int(address)
        result = (self.cpu.x - value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.x >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 4

    def cpy_immediate(self) -> None:
        immediate_value = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        result = (self.cpu.y - immediate_value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.y >= immediate_value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 2

    def cpy_zero_page(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address)
        result = (self.cpu.y - value) & 0xFF
        self.cpu.status = (
            (self.cpu.status | 0x01)
            if self.cpu.y >= value
            else (self.cpu.status & ~0x01)
        )  # Carry flag (Bit 0)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 3

    def adc_immediate(self) -> None:
        value = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        carry_in = 1 if (self.cpu.status & 0x01) else 0  # Carry flag (Bit 0)
        decimal_mode = (self.cpu.status & 0x08) != 0  # Decimal Mode flag (Bit 3)

        if not decimal_mode:
            result = self.cpu.a + value + carry_in

            # Set flags directly in self.cpu.status
            self.cpu.status = (
                (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
            )  # Carry flag
            self.cpu.status = (
                (self.cpu.status | 0x02)
                if (result & 0xFF) == 0
                else (self.cpu.status & ~0x02)
            )  # Zero flag
            self.cpu.status = (
                (self.cpu.status | 0x80)
                if (result & 0x80)
                else (self.cpu.status & ~0x80)
            )  # Negative flag
            overflow = (((self.cpu.a ^ value) & 0x80) == 0) and (
                ((self.cpu.a ^ result) & 0x80) != 0
            )
            self.cpu.status = (
                (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
            )  # Overflow flag
            self.cpu.a = result & 0xFF
        else:
            # BCD mode addition
            temp = (self.cpu.a & 0x0F) + (value & 0x0F) + carry_in
            carry_nibble = 1 if temp > 9 else 0
            if temp > 9:
                temp += 6
            temp2 = (self.cpu.a & 0xF0) + (value & 0xF0) + (carry_nibble << 4)
            carry_out = 1 if temp2 > 0x90 else 0
            if temp2 > 0x90:
                temp2 += 0x60

            result_bcd = (temp & 0x0F) | (temp2 & 0xF0)
            # Set flags directly in self.cpu.status
            self.cpu.status = (
                (self.cpu.status | 0x01) if carry_out else (self.cpu.status & ~0x01)
            )  # Carry flag
            self.cpu.status = (
                (self.cpu.status | 0x02)
                if (result_bcd & 0xFF) == 0
                else (self.cpu.status & ~0x02)
            )  # Zero flag
            self.cpu.status = (
                (self.cpu.status | 0x80)
                if (result_bcd & 0x80)
                else (self.cpu.status & ~0x80)
            )  # Negative flag
            self.cpu.a = result_bcd & 0xFF
        self.cpu.cycles += 2

    def adc_zero_page(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(zero_page_address)
        carry = 1 if (self.cpu.status & 0x01) else 0  # Carry flag (Bit 0)
        result = self.cpu.a + value + carry
        self.cpu.status = (
            (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
        )  # Carry flag
        self.cpu.status = (
            (self.cpu.status | 0x02)
            if (result & 0xFF) == 0
            else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag

        overflow = (~(self.cpu.a ^ value) & (self.cpu.a ^ result) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )  # Overflow flag
        self.cpu.a = result & 0xFF  # Truncate to 8 bits
        self.cpu.cycles += 3

    def adc_absolute_y(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.cycles += 4 + (
            1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
        )
        value = self.cpu.read_memory_int(effective_address)
        carry = 1 if (self.cpu.status & 0x01) else 0  # Carry flag (Bit 0)
        result = self.cpu.a + value + carry
        self.cpu.status = (
            (self.cpu.status | 0x01) if result > 0xFF else (self.cpu.status & ~0x01)
        )  # Carry flag
        self.cpu.status = (
            (self.cpu.status | 0x02)
            if (result & 0xFF) == 0
            else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag
        overflow = (~(self.cpu.a ^ value) & (self.cpu.a ^ result) & 0x80) != 0
        self.cpu.status = (
            (self.cpu.status | 0x40) if overflow else (self.cpu.status & ~0x40)
        )  # Overflow flag
        self.cpu.a = result & 0xFF  # Truncate to 8 bits
