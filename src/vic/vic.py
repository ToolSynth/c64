from multiprocessing.shared_memory import SharedMemory
from typing import TYPE_CHECKING

import numpy as np
from numpy import uint8

from src.utils.log_setup import log

if TYPE_CHECKING:
    from src.bus.bus import Bus


class VIC:
    """Represents the VIC-II graphics chip in the Commodore 64 emulator."""

    def __init__(self, bus: "Bus", mode: str = "PAL") -> None:
        """
        Initializes the VIC-II.

        :param bus: The system bus instance.
        :param mode: "PAL" (default) or "NTSC".
        """
        self.bus: Bus = bus
        self.current_line: int = 0
        self.raster_interrupt_line: int = 0
        self.overflow_cycles: int = 0

        self.mode: str = mode
        self.total_lines: int = 311 if mode == "PAL" else 262
        self.cycles_per_line: int = 63 if mode == "PAL" else 65

        self.size: int = 0x2F  # Register size (0x2F = 47)
        self.shm: SharedMemory = SharedMemory(create=True, size=self.size)
        self.registers: np.ndarray = np.ndarray(
            (self.size,), dtype=np.uint8, buffer=self.shm.buf
        )
        self.registers.fill(0x00)
        self.registers[0x1A] = 0xFF  # Default interrupt enable mask

        self.ready_frame: bool = False
        self.update_raster_interrupt_line()
        log.info("VIC initialization complete.")

    def generate_raster_interrupt(self) -> None:
        """Generates a raster interrupt when conditions are met."""
        interrupt_enable: int = self.registers[0x1A] & 0x01
        if interrupt_enable != 0 and self.current_line == self.raster_interrupt_line:
            self.registers[0x19] |= 0x01
            log.debug(f"Raster interrupt generated at line {self.current_line}.")
            self.bus.trigger_irq()

    def update_raster_interrupt_line(self) -> None:
        """Updates the raster interrupt line based on VIC-II registers."""
        low_byte: int = self.registers[0x12]
        high_bit: int = (self.registers[0x11] & 0x80) >> 7
        self.raster_interrupt_line = (high_bit << 8) | low_byte
        log.debug(f"Updated Raster Interrupt Line: {self.raster_interrupt_line}")

    def tick(self) -> None:
        """Handles the VIC-II timing cycle."""
        if self.overflow_cycles >= self.cycles_per_line:
            self._tick()
            self.overflow_cycles = 0
        self.overflow_cycles += self.bus.cpu.delta_cycles

    def _tick(self) -> None:
        """Processes a single VIC-II scanline."""
        self.current_line += 1

        if self.current_line >= self.total_lines:
            self.current_line = 0
            self.ready_frame = True

        self.write(0xD012, self.current_line & 0xFF)

        if self.current_line >= 256:
            self.write(0xD011, (self.registers[0x11] | 0x80))
        else:
            self.registers[0x11] &= 0x7F
            self.write(0xD011, self.registers[0x11])

        if self.current_line == self.raster_interrupt_line:
            self.generate_raster_interrupt()

    def read(self, address: int) -> uint8:
        """
        Reads a byte from a VIC-II register.

        :param address: The address to read from.
        :return: The value stored in the register.
        """
        offset: int = address - 0xD000
        if 0 <= offset < len(self.registers):
            value: uint8 = self.registers[offset]
            return value

        log.warning(f"Read from invalid VIC register address: {hex(address)}")
        return uint8(0)

    def write(self, address: int, value: int) -> None:
        """
        Writes a byte to a VIC-II register.

        :param address: The address to write to.
        :param value: The value to be written.
        """
        offset: int = address - 0xD000

        if 0 <= offset < len(self.registers):
            self.registers[offset] = value & 0xFF
            log.debug(
                f"VIC Register WRITE - Address: {hex(address)}, Value: {hex(value)}"
            )

            if offset in (0x11, 0x12):
                self.update_raster_interrupt_line()
            elif address == 0xD019:
                self.registers[0x19] &= ~value & 0xFF  # Clear interrupt flags

            return

        log.warning(f"Write to invalid VIC register address: {hex(address)}")

    def __getstate__(self) -> dict[str, int | str]:
        """Returns the state for serialization."""
        return {"size": self.size, "shm_name": self.shm.name}

    def __setstate__(self, state: dict[str, int | str]) -> None:
        """Restores the state from serialization."""
        self.size = state["size"]
        self.shm = SharedMemory(name=state["shm_name"])
        self.registers = np.ndarray((self.size,), dtype=np.uint8, buffer=self.shm.buf)

    def close(self) -> None:
        """Closes access to shared memory."""
        try:
            self.shm.unlink()
            log.debug("Shared memory unlinked.")
        except FileNotFoundError:
            log.debug("Shared memory closed.")

    def __del__(self) -> None:
        """Ensures that the process is stopped if the proxy is destroyed."""
        self.close()
