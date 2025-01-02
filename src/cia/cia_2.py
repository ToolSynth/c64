from multiprocessing.shared_memory import SharedMemory
from typing import TYPE_CHECKING

import numpy as np
from numpy import uint8

from src.utils.log_setup import log

if TYPE_CHECKING:
    from src.bus.bus import Bus


class CIA2:
    def __init__(self, bus: "Bus") -> None:
        """Initializes the CIA2 chip with a shared memory buffer."""
        self.bus: Bus = bus
        self.size: int = 16
        self.shm: SharedMemory = SharedMemory(create=True, size=self.size)
        self.registers: np.ndarray = np.ndarray(
            (self.size,), dtype=np.uint8, buffer=self.shm.buf
        )
        log.debug("CIA2 initialized.")

    def read(self, address: int) -> uint8:
        """
        Reads a value from a CIA2 register.

        :param address: The memory address to read from.
        :return: The value stored at the given address.
        """
        offset: int = address & 0x0F

        if offset == 0x00:
            value: uint8 = self.registers[0x00]
            log.debug(f"CIA2 READ PORT A: Value={hex(value)}")
            return value

        return self.registers[offset]

    def write(self, address: int, value: int) -> None:
        """
        Writes a value to a CIA2 register.

        :param address: The memory address to write to.
        :param value: The value to be written.
        """
        offset: int = address & 0x0F

        if offset == 0x00:
            self.registers[0x00] = value
            log.info(f"WRITE CIA2 address: {address}: Value={hex(value)}")

        self.registers[offset] = value

    def tick(self) -> None:
        """Performs a clock tick operation (not implemented)."""

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
