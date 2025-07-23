from multiprocessing.shared_memory import SharedMemory

import numpy as np

from src.bus.memory.base import BaseMemory
from src.utils.log_setup import log


class RAM(BaseMemory):
    def __init__(self) -> None:
        """Initializes the RAM with a shared memory buffer."""
        self.size: int = 65536
        self.shm: SharedMemory = SharedMemory(create=True, size=self.size)
        self.data: np.ndarray = np.ndarray(
            (self.size,), dtype=np.uint8, buffer=self.shm.buf
        )
        log.info("RAM initialization complete.")
        self.reset()

    def read(self, address: int) -> int | np.uint8:
        """Reads a byte from the specified memory address."""
        value: int = self.data[address]
        return value

    def write(self, address: int, value: int) -> None:
        """Writes a byte to the specified memory address."""
        self.data[address] = value

    def reset(self) -> None:
        """Initializes all RAM to zero."""
        self.data.fill(0x00)
        log.debug("RAM initialized to zeros.")

    def get_memory_usage(
        self, *, include_addresses: bool = False
    ) -> dict[str, int | list[str]]:
        """
        Calculates the used and free space in RAM.

        :param include_addresses: If True, returns a list of occupied addresses.
        :return: Dictionary with 'total', 'used', 'free', and optionally 'addresses'.
        :raises MemoryError: If all RAM is full.
        """
        total: int = len(self.data)
        used: int = np.count_nonzero(self.data)
        free: int = total - used

        if free == 0:
            raise MemoryError(
                "Memory is completely full. No free space available in RAM."
            )

        usage: dict[str, int | list[str]] = {
            "total": total,
            "used": used,
            "free": free,
        }

        if include_addresses:
            used_addresses: list[str] = [
                hex(i) for i in range(total) if self.data[i] != 0
            ]
            usage["addresses"] = used_addresses

        log.debug(f"Memory Usage - Total: {total}, Used: {used}, Free: {free}")
        return usage

    def read_range(self, start_address: int, end_address: int) -> list[int]:
        """
        Reads a range of memory values.

        :param start_address: Starting address of the range.
        :param end_address: Ending address of the range.
        :return: List of memory values in the specified range.
        :raises ValueError: If start_address > end_address.
        """
        if start_address > end_address:
            raise ValueError(
                f"Start address {hex(start_address)} cannot be greater than end address {hex(end_address)}"
            )

        memory_values: list[int] = []
        for address in range(start_address, end_address + 1):
            value: int = self.read(address)
            memory_values.append(value)
        return memory_values

    def __getstate__(self) -> dict[str, int | str]:
        """Returns the state for serialization."""
        return {"size": self.size, "shm_name": self.shm.name}

    def __setstate__(self, state: dict[str, int | str]) -> None:
        """Restores the state from serialization."""
        self.size = state["size"]
        self.shm = SharedMemory(name=state["shm_name"])
        self.data = np.ndarray((self.size,), dtype=np.uint8, buffer=self.shm.buf)

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
