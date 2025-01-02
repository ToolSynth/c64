from typing import TYPE_CHECKING

import numpy as np

from src.utils.log_setup import log

if TYPE_CHECKING:
    from src.bus.bus import Bus


class SID:
    def __init__(self, bus: "Bus") -> None:
        """Initializes the SID chip."""
        self.bus = bus
        self.registers = np.zeros(32, dtype=np.uint8)
        log.info("SID initialization complete.")

    def read(self, address: int) -> int | np.uint8:
        """
        Reads a value from a SID register.

        :param address: Offset (0x00-0x1F) in the SID register space.
        """
        offset = address - 0xD400
        if 0 <= offset < 32:
            value = self.registers[offset]
            log.debug(f"SID READ Register: Address={hex(offset)}, Value={hex(value)}")
            return value
        log.warning(f"SID READ out of bounds: Address={hex(offset)}")
        return 0xFF

    def write(self, address: int, value: int | np.uint8) -> None:
        """
        Writes a value to a SID register.

        :param address: Offset (0x00-0x1F) in the SID register space.
        :param value: Value to write.
        """
        offset = address - 0xD400
        if 0 <= offset < 32:
            self.registers[offset] = value
            log.debug(f"SID WRITE Register: Address={hex(offset)}, Value={hex(value)}")
            self.handle_audio_update(offset, value)
        else:
            log.warning(
                f"SID WRITE out of bounds: Address={hex(address)}, Value={hex(value)}"
            )

    def handle_audio_update(self, address: int, value: int | np.uint8) -> None:
        """
        Processes changes to audio registers.

        This is where audio wave generation emulation logic can be implemented.
        """
        log.debug(
            f"SID Audio Update Triggered: Address={hex(address)}, Value={hex(value)}"
        )

    def tick(self) -> None:
        """
        Simulates one cycle of the SID.

        In a real SID, this would involve handling filters and generating sound.
        """
        log.debug("SID Tick: Processing audio")
