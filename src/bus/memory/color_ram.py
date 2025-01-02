from multiprocessing.shared_memory import SharedMemory

import numpy as np

from src.utils.log_setup import log

from .base import BaseMemory


class ColorRAM(BaseMemory):
    def __init__(self) -> None:
        self.size: int = 1024
        self.shm: SharedMemory = SharedMemory(
            create=True, size=self.size
        )  # Create SharedMemory
        self.data: np.ndarray = np.ndarray(
            (self.size,), dtype=np.uint8, buffer=self.shm.buf
        )
        log.info("Color RAM initialization complete.")

    def _offset(self, address: int) -> int:
        return address - 0xD800

    def read(self, address: int) -> np.uint8:
        """
        Reads from Color RAM. The address is limited to 10 bits (0xD800 - 0xDBFF).

        Physically, this is 4-bit memory, with upper bits "open" (open bus).
        A common approach is to return (color_ram[offset] | 0xF0) or just color_ram[offset].
        In simpler emulators, returning just the value works.
        """
        return self.data[self._offset(address)] & 0x0F

    def write(self, address: int, value: int) -> None:
        """Writes to Color RAM. Only the lower 4 bits of the value are stored."""
        self.data[self._offset(address)] = value & 0x0F

    def __getstate__(self) -> dict[str, int | str]:
        return {"size": self.size, "shm_name": self.shm.name}

    def __setstate__(self, state: dict[str, int | str]) -> None:
        self.size = state["size"]
        self.shm = SharedMemory(name=state["shm_name"])
        self.data = np.ndarray((self.size,), dtype=np.uint8, buffer=self.shm.buf)

    def close(self) -> None:
        """Close access to shared memory."""
        try:
            self.shm.unlink()
            log.debug("Shared memory unlinked.")
        except FileNotFoundError:
            log.debug("Shared memory closed.")

    def __del__(self) -> None:
        """Ensure that the process is stopped if the proxy is destroyed."""
        self.close()
