from typing import TYPE_CHECKING

from src.cpu.manager import InstructionManager
from src.utils.log_setup import log

if TYPE_CHECKING:
    from src.bus.bus import Bus


class CPU:
    def __init__(self, bus: "Bus") -> None:
        self.bus = bus
        self.a = 0x00  # Accumulator
        self.x = 0x00  # Register X
        self.y = 0x00  # Register Y
        self.sp = 0xFF  # Stack Pointer
        self.pc = 0xFF  # Program Counter
        self.status = 0x00  # Status Flags
        self._pla_register = 0x00
        self.cycles = 0x00
        self.previous_cycles = 0x00
        self.delta_cycles = 0x00
        self.instruction_manager = InstructionManager(self)
        log.debug("CPU initialization complete.")

    def execute_next_instruction(self) -> None:
        """Executes the next CPU instruction."""
        opcode = self.bus.read(self.pc)
        self.pc = (self.pc + 1) & 0xFFFF
        self.previous_cycles = self.cycles
        self.instruction_manager.execute(opcode)
        self.delta_cycles = self.cycles - self.previous_cycles

    def format_status_for_log(self) -> list[tuple[str, int]]:
        """
        Formats the status register in the NV-BDIZC layout (typical for the 6502).
        Bit indices: 7=N, 6=V, 5=U, 4=B, 3=D, 2=I, 1=Z, 0=C
        """
        n = (self.status >> 7) & 1
        v = (self.status >> 6) & 1
        b = (self.status >> 4) & 1
        d = (self.status >> 3) & 1
        i = (self.status >> 2) & 1
        z = (self.status >> 1) & 1
        c = (self.status >> 0) & 1

        return [
            ("N", n),
            ("V", v),
            ("-", 0),  # Unused bit 5
            ("B", b),
            ("D", d),
            ("I", i),
            ("Z", z),
            ("C", c),
        ]

    def read_memory_int(self, address: int) -> int:
        value = self.bus.read(address)
        if isinstance(value, int):
            return value
        return int(value)

    def read_word_le(self, address: int) -> int:
        low = self.read_memory_int(address)
        high = self.read_memory_int((address + 1) & 0xFFFF)
        return ((high << 8) | low) & 0xFFFF

    @property
    def pla_register(self) -> int:
        """Gets the $0001 (CPU I/O Port) register."""
        return self._pla_register

    @pla_register.setter
    def pla_register(self, value: int) -> None:
        """Sets the $0001 (CPU I/O Port) register with 8-bit constraints."""
        value = int(value) & 0xFF
        if not (0x00 <= value <= 0xFF):
            log.error(f"Invalid CPU port 01 value: {value:#04X}")
            raise ValueError("CPU port 01 out of bounds")

        self._pla_register = value
        log.debug(
            f"Setting CPU port 01: Old={self._pla_register:#04X}, New={value:#04X}"
        )

    def handle_irq(self) -> None:
        """Handles IRQ interrupt."""
        if not (self.status & (1 << 2)):
            self.push((self.pc >> 8) & 0xFF)  # high byte PC
            self.push(self.pc & 0xFF)  # low byte PC
            self.push(self.status)  # status register
            self.status |= 1 << 2
            irq_address = self.read_memory_int(0xFFFE) | (
                self.read_memory_int(0xFFFF) << 8
            )
            self.pc = irq_address

    def handle_nmi(self) -> None:
        """Handles Non-Maskable Interrupt (NMI)."""
        self.push((self.pc >> 8) & 0xFF)
        self.push(self.pc & 0xFF)
        self.push(self.status)
        self.status |= 1 << 2
        nmi_address = self.read_memory_int(0xFFFA) | (self.read_memory_int(0xFFFB) << 8)
        self.pc = nmi_address

    def push(self, value: int) -> None:
        """Pushes a value onto the stack."""
        if self.sp < 0x00:
            log.error("Stack overflow: Cannot push to stack")
            raise OverflowError("Stack overflow: Cannot push to stack")
        self.bus.ram.write(0x0100 + self.sp, value)
        self.sp = (self.sp - 1) & 0xFF

    def pull(self) -> int:
        """Pulls a value from the stack."""
        if self.sp >= 0xFF:
            log.error("Stack underflow: Cannot pull from stack")
            raise OverflowError("Stack underflow: Cannot pull from stack")
        self.sp = (self.sp + 1) & 0xFF
        return self.read_memory_int(0x0100 + self.sp)

    def reset(self) -> None:
        """Resets the CPU and sets PC to the reset vector address."""
        self.sp = 0xFF
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.status = 0x34
        self.bus.write(0x0001, 0x37)
        self.pc = self.read_word_le(0xFFFC)
