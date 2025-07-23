from typing import TYPE_CHECKING

import numpy as np

from src.utils.log_setup import log

from .tod_clock import Timer

if TYPE_CHECKING:
    from src.bus.bus import Bus


class CIA1:
    def __init__(self, bus: "Bus", name: str = "CIA", mode: str = "PAL") -> None:
        self.bus = bus
        self.name = name
        self.registers = np.zeros(16, dtype=np.uint8)

        # Timers and interrupts
        self.timer_a = Timer(name="Timer A", mode=mode, irq_bit=0)
        self.timer_b = Timer(name="Timer B", mode=mode, irq_bit=1)
        self.interrupt_flags = 0

        # --- [NEW: DDR and latch] ---
        self.ddra = 0x00  # Data Direction Register for port A
        self.ddrb = 0x00  # Data Direction Register for port B
        self.latch_a = 0xFF  # Last written value to port A (output)
        self.latch_b = 0xFF  # Last written value to port B (output)

        # Assumption: if DDR=0 (input), it has a pull-up -> read bit as 1
        log.debug(f"{name} initialized in {mode} mode.")

    def read_port_a(self) -> int:
        """
        Returns the value considering DDR:
        - bits where DDR=1 -> return latch_a
        - bits where DDR=0 -> assume pull-up (1) or another input state
        """
        result = 0
        for bit in range(8):
            mask = 1 << bit
            if (self.ddra & mask) != 0:
                # Output bit -> return value from latch_a
                if (self.latch_a & mask) != 0:
                    result |= mask
            else:
                # Input bit -> assume default 1 (pull-up)
                # Modify if simulating a different state
                result |= mask
        return result

    def read_port_b(self) -> int:
        """Similar logic for port B."""
        result = 0
        for bit in range(8):
            mask = 1 << bit
            if (self.ddrb & mask) != 0:
                # Output bit
                if (self.latch_b & mask) != 0:
                    result |= mask
            else:
                # Input bit (pull-up)
                result |= mask
        return result

    def write_port_a(self, value: int) -> None:
        """Write to port A: only bits where DDR=1 overwrite latch_a."""
        old = self.latch_a
        self.latch_a = (old & ~self.ddra) | (value & self.ddra)
        log.debug(
            f"{self.name} WRITE PORT A: old={hex(old)}, new={hex(self.latch_a)}, "
            f"written={hex(value)}, DDR={hex(self.ddra)}"
        )

    def write_port_b(self, value: int) -> None:
        """Write to port B: only bits where DDR=1 overwrite latch_b."""
        old = self.latch_b
        self.latch_b = (old & ~self.ddrb) | (value & self.ddrb)
        log.debug(
            f"{self.name} WRITE PORT B: old={hex(old)}, new={hex(self.latch_b)}, "
            f"written={hex(value)}, DDR={hex(self.ddrb)}"
        )

    def read(self, address: int) -> int:
        offset = address & 0x0F
        read_functions = {
            0x00: self.read_port_a,
            0x01: self.read_port_b,
            0x02: lambda: self.ddra,
            0x03: lambda: self.ddrb,
            0x0D: lambda: self.interrupt_flags,
            0x04: lambda: self.timer_a.low_byte,
            0x05: lambda: self.timer_a.high_byte,
            0x06: lambda: self.timer_b.low_byte,
            0x07: lambda: self.timer_b.high_byte,
            0x0E: lambda: self.timer_a.control_register,
            0x0F: lambda: self.timer_b.control_register,
        }
        value = read_functions.get(offset, lambda: self.registers[offset])()
        log.debug(f"{self.name} READ Address={hex(offset)}, Value={hex(value)}")
        return value

    def write(self, address: int, value: int) -> None:
        offset = address & 0x0F
        write_functions = {
            0x00: lambda v: self.write_port_a(v),
            0x01: lambda v: self.write_port_b(v),
            0x02: lambda v: self._set_register("DDRA", "ddra", v),
            0x03: lambda v: self._set_register("DDRB", "ddrb", v),
            0x0D: lambda v: self._clear_interrupt_flags(v),
            0x04: lambda v: self.timer_a.configure(low_byte=v),
            0x05: lambda v: self.timer_a.configure(high_byte=v),
            0x06: lambda v: self.timer_b.configure(low_byte=v),
            0x07: lambda v: self.timer_b.configure(high_byte=v),
            0x0E: lambda v: self.timer_a.configure(
                force_load=bool(v & 0x10), start=bool(v & 0x01)
            ),
            0x0F: lambda v: self.timer_b.configure(
                force_load=bool(v & 0x10), start=bool(v & 0x01)
            ),
        }
        write_functions.get(offset, lambda v: self.registers.__setitem__(offset, v))(
            value
        )
        log.debug(
            f"{self.name} WRITE Register: Address={hex(offset)}, Value={hex(value)}"
        )

    def _set_register(self, name: str, attr: str, value: int) -> None:
        setattr(self, attr, value)
        log.debug(f"{self.name} WRITE {name}: Value={hex(value)}")

    def _clear_interrupt_flags(self, value: int) -> None:
        self.registers[0x0D] = value & 0xFF
        log.debug(f"{self.name} CLEAR Interrupt Flags with Mask: {bin(value)}")

    def tick(self) -> None:
        self.timer_a.tick(self.bus.cpu.delta_cycles)
        self.timer_b.tick(self.bus.cpu.delta_cycles)

        if self.timer_a.interrupt_triggered:
            self.trigger_timer_interrupt("A")
            self.timer_a.clear_interrupt()

        if self.timer_b.interrupt_triggered:
            self.trigger_timer_interrupt("B")
            self.timer_b.clear_interrupt()

    def trigger_timer_interrupt(self, timer_name: str) -> None:
        timer = self.timer_a if timer_name == "A" else self.timer_b
        self.interrupt_flags |= 1 << timer.irq_bit  # Set interrupt flag
        log.debug(
            f"{self.name} Timer {timer_name} IRQ triggered. "
            f"Timer irq_bit: {(1 << timer.irq_bit)} "
            f"Interrupt_flags: {self.interrupt_flags}"
        )

        if self.interrupt_flags & (1 << timer.irq_bit) != 0:
            log.debug(f"{self.name} Timer {timer_name} IRQ processed.")
            self.bus.trigger_irq()
