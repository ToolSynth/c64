from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from src.utils.log_setup import log


@dataclass
class ROM:
    filepath: str
    size: int
    start_address: int
    data: bytes | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        """Loads data from the binary ROM file and assigns it to the 'data' attribute."""
        try:
            with Path.open(self.filepath, "rb") as file:
                self.data = file.read(self.size)
                log.debug(f"ROM loaded: {self.filepath}")
                self.verify_size(self.data)
                log.debug(f"ROM size verified: {self.filepath}")
        except FileNotFoundError as err:
            raise RuntimeError(f"ROM file not found: {self.filepath}") from err

    def verify_size(self, rom: bytes) -> None:
        """
        Verifies the size of the loaded ROM against the expected size.

        :param rom: The loaded ROM data.
        :raises ValueError: If the ROM size does not match the expected size.
        """
        if len(rom) != self.size:
            raise ValueError(
                f"Invalid ROM size for {self.filepath}, "
                f"expected: {self.size}, actual: {len(rom)}"
            )

    def read(self, address: np.uint8 | int) -> np.uint8:
        """Reads a byte from the ROM at the specified address."""
        if self.data is None:
            raise ValueError(f"ROM data is not loaded: {self.filepath}")
        return self.data[address - self.start_address]

    def write(self, address: int, value: int) -> None:
        """
        Prevents write operations on ROM.

        :raises PermissionError: Since ROM is read-only.
        """
        raise PermissionError(
            f"Write operation not permitted on ROM ({self.filepath}). "
            f"Address: {hex(address)}, value: {hex(value)}"
        )

    def __bytes__(self) -> bytes:
        """Returns ROM data as bytes."""
        if self.data is None:
            raise ValueError(f"ROM data is not loaded: {self.filepath}")
        return self.data
