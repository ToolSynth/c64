from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cpu.cpu import CPU


class Heap:
    def __init__(self, cpu: "CPU") -> None:
        self.cpu = cpu

    def lda_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        value = self.cpu.read_memory_int(address)
        self.cpu.a = value
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 3

    def lda_zeropage_x(self) -> None:
        base_address = self.cpu.read_memory_int(self.cpu.pc)
        effective_address = (base_address + self.cpu.x) & 0xFF
        value = self.cpu.read_memory_int(effective_address)
        self.cpu.a = value
        self.cpu.pc += 1
        self.cpu.cycles += 4
        # Set flags directly in self.cpu.status
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)

    def lda_indirect_y(self) -> None:
        zp_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        base_address = self.cpu.read_word_le(zp_address)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.cycles += 5 + (
            1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
        )
        value = self.cpu.read_memory_int(effective_address)
        self.cpu.a = value
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)

    def lda_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        self.cpu.a = self.cpu.read_memory_int(address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 4

    def lda_immediate(self) -> None:
        self.cpu.a = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 2

    def lda_absolute_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        target_address = (base_address + self.cpu.x) & 0xFFFF
        self.cpu.cycles += 4 + (
            1 if (base_address & 0xFF00) != (target_address & 0xFF00) else 0
        )
        self.cpu.a = self.cpu.read_memory_int(target_address)
        self.cpu.pc += 2
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)

    def lda_absolute_y(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.cycles += 4 + (
            1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
        )
        self.cpu.a = self.cpu.read_memory_int(effective_address)
        self.cpu.pc += 2
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.a == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.a & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)

    def sta_zeropage_x(self) -> None:
        base_address = self.cpu.read_memory_int(self.cpu.pc)
        effective_address = (base_address + self.cpu.x) & 0xFF
        self.cpu.bus.write(effective_address, self.cpu.a)
        self.cpu.pc += 1
        self.cpu.cycles += 4

    def sta_indirect_y(self) -> None:
        zero_page_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        base_address = self.cpu.read_word_le(zero_page_address)
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.bus.write(effective_address, self.cpu.a)
        self.cpu.cycles += 6

    def sta_absolute_y(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        target_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.bus.write(target_address, self.cpu.a)
        self.cpu.pc += 2
        self.cpu.cycles += 5

    def sta_zero_page(self) -> None:
        target_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.bus.write(target_address, self.cpu.a)
        self.cpu.cycles += 3

    def sta_absolute(self) -> None:
        target_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.bus.write(target_address, self.cpu.a)
        self.cpu.pc += 2
        self.cpu.cycles += 4

    def sta_absolute_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        effective_address = (base_address + self.cpu.x) & 0xFFFF
        self.cpu.bus.write(effective_address, self.cpu.a)
        self.cpu.pc += 2
        self.cpu.cycles += 5

    def ldx_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.x = self.cpu.read_memory_int(address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.x == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.x & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 3

    def ldx_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        self.cpu.x = self.cpu.read_memory_int(address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.x == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.x & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 4

    def ldx_immediate(self) -> None:
        self.cpu.x = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.x == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.x & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 2

    def ldx_absolute_y(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        effective_address = (base_address + self.cpu.y) & 0xFFFF
        self.cpu.x = self.cpu.read_memory_int(effective_address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.x == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.x & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 4 + (
            1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
        )

    def stx_zero_page_y(self) -> None:
        effective_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.y) & 0xFF
        self.cpu.bus.write(effective_address, self.cpu.x)
        self.cpu.pc += 1
        self.cpu.cycles += 4

    def stx_zero_page(self) -> None:
        self.cpu.bus.write(self.cpu.read_memory_int(self.cpu.pc), self.cpu.x)
        self.cpu.pc += 1
        self.cpu.cycles += 3

    def stx_absolute(self) -> None:
        target_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.bus.write(target_address, self.cpu.x)
        self.cpu.pc += 2
        self.cpu.cycles += 4

    def ldy_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.y = self.cpu.read_memory_int(address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.y == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.y & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 3

    def ldy_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.y = self.cpu.read_memory_int(address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.y == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.y & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.pc += 2
        self.cpu.cycles += 4

    def ldy_zero_page_x(self) -> None:
        effective_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        self.cpu.y = self.cpu.read_memory_int(effective_address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.y == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.y & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 4

    def ldy_immediate(self) -> None:
        self.cpu.y = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.y == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.y & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 2

    def ldy_absolute_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        effective_address = (base_address + self.cpu.x) & 0xFFFF
        self.cpu.y = self.cpu.read_memory_int(effective_address)
        self.cpu.status = (
            (self.cpu.status | 0x02) if self.cpu.y == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80)
            if (self.cpu.y & 0x80)
            else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.pc += 2
        self.cpu.cycles += 4 + (
            1 if (base_address & 0xFF00) != (effective_address & 0xFF00) else 0
        )  # Extra cycle for page crossing

    def sty_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.bus.write(address, self.cpu.y)
        self.cpu.pc += 2
        self.cpu.cycles += 4

    def sty_zero_page_x(self) -> None:
        target_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.bus.write(target_address, self.cpu.y)
        self.cpu.pc += 1
        self.cpu.cycles += 4

    def sty_zero_page(self) -> None:
        self.cpu.bus.write(self.cpu.read_memory_int(self.cpu.pc), self.cpu.y)
        self.cpu.pc += 1
        self.cpu.cycles += 3

    def dec_zero_page(self) -> None:
        address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        result = (self.cpu.read_memory_int(address) - 1) & 0xFF
        self.cpu.bus.write(address, result)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 5

    def dec_absolute(self) -> None:
        address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        result = (self.cpu.read_memory_int(address) - 1) & 0xFF
        self.cpu.bus.write(address, result)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 6

    def inc_absolute_x(self) -> None:
        base_address = self.cpu.read_word_le(self.cpu.pc)
        target_address = (base_address + self.cpu.x) & 0xFFFF
        self.cpu.pc += 2
        result = (self.cpu.read_memory_int(target_address) + 1) & 0xFF
        self.cpu.bus.write(target_address, result)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag (Bit 1)
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag (Bit 7)
        self.cpu.cycles += 7

    def inc_zero_page_x(self) -> None:
        target_address = (self.cpu.read_memory_int(self.cpu.pc) + self.cpu.x) & 0xFF
        self.cpu.pc += 1
        result = (self.cpu.read_memory_int(target_address) + 1) & 0xFF
        self.cpu.bus.write(target_address, result)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 6

    def inc_zero_page(self) -> None:
        target_address = self.cpu.read_memory_int(self.cpu.pc)
        self.cpu.pc += 1
        result = (self.cpu.read_memory_int(target_address) + 1) & 0xFF
        self.cpu.bus.write(target_address, result)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 5

    def inc_absolute(self) -> None:
        target_address = self.cpu.read_word_le(self.cpu.pc)
        self.cpu.pc += 2
        result = (self.cpu.read_memory_int(target_address) + 1) & 0xFF
        self.cpu.bus.write(target_address, result)
        self.cpu.status = (
            (self.cpu.status | 0x02) if result == 0 else (self.cpu.status & ~0x02)
        )  # Zero flag
        self.cpu.status = (
            (self.cpu.status | 0x80) if (result & 0x80) else (self.cpu.status & ~0x80)
        )  # Negative flag
        self.cpu.cycles += 6
