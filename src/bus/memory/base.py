from abc import ABC, abstractmethod

import numpy as np


class BaseMemory(ABC):
    """Abstract class for memory management."""

    @abstractmethod
    def read(self, address: int) -> int | np.uint8:
        """
        Reads a byte from memory.

        :param address: Address to read from.
        :return: Byte value at the specified address.
        """

    @abstractmethod
    def write(self, address: int | np.uint8, value: int | np.uint8 | np.uint16) -> None:
        """
        Writes a byte to memory.

        :param address: Address to write to.
        :param value: Byte value to write.
        """
