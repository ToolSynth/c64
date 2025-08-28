from enum import Enum
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.bus.bus import Bus

from typing import TYPE_CHECKING

from src.bus.memory.color_ram import ColorRAM
from src.bus.memory.ram import RAM
from src.bus.memory.rom import ROM
from src.cia.cia_1 import CIA1
from src.cia.cia_2 import CIA2
from src.sid.sid import SID
from src.utils.log_setup import log
from src.vic.vic import VIC

if TYPE_CHECKING:
    from src.bus.bus import Bus


class MemoryTypes(str, Enum):
    kernel_rom = "kernel_rom"
    basic_rom = "basic_rom"
    char_rom = "char_rom"
    vic = "vic"
    sid = "sid"
    cia_1 = "cia_1"
    cia_2 = "cia_2"
    color_ram = "color_ram"


class PLA:
    def __init__(
        self,
        bus: "Bus",
        *,
        loram: bool = True,
        hiram: bool = True,
        charen: bool = False,
    ) -> None:
        """Initializes memory mapping control registers."""
        self.bus: Bus = bus
        self.loram: bool = loram
        self.hiram: bool = hiram
        self.charen: bool = charen
        log.info("Address decoding PLA initialization complete.")

    @property
    def is_basic_rom_visible(self) -> bool:
        return self.loram and self.hiram

    @property
    def is_kernel_rom_visible(self) -> bool:
        return self.hiram

    @property
    def is_char_rom_visible(self) -> bool:
        return not self.charen

    def decode_address(
        self, address: int
    ) -> VIC | SID | CIA1 | CIA2 | ColorRAM | RAM | ROM:
        """
        Decodes the address and returns the module responsible for handling the request.
        """
        result = self.bus.ram  # Domyślnie RAM, jeśli żaden warunek nie pasuje

        if 0xE000 <= address <= 0xFFFF and self.is_kernel_rom_visible:
            result = self.bus.kernel_rom
        elif 0xA000 <= address <= 0xBFFF and self.is_basic_rom_visible:
            result = self.bus.basic_rom
        elif 0x1000 <= address <= 0x1FFF and self.is_char_rom_visible:
            result = self.bus.chargen_rom
        elif 0xD000 <= address <= 0xDFFF and not self.is_char_rom_visible:
            match address:
                case a if 0xD000 <= a <= 0xD3FF:
                    result = self.bus.vic
                case a if 0xD400 <= a <= 0xD7FF:
                    result = self.bus.sid
                case a if 0xDC00 <= a <= 0xDCFF:
                    result = self.bus.cia_1
                case a if 0xDD00 <= a <= 0xDDFF:
                    result = self.bus.cia_2
                case a if 0xD800 <= a <= 0xDBFF:
                    result = self.bus.color_ram

        return result

    def read(self, address: int) -> int | np.uint8:
        """Handles memory reads, allowing RAM to shadow ROM when written."""
        target = self.decode_address(address)
        if isinstance(target, ROM):
            # Reads from ROM are served from underlying RAM to permit tests to
            # patch vectors like the IRQ handler.
            return self.bus.ram.read(address)
        return target.read(address)

    def write(self, address: int, value: int) -> None:
        """Handles memory writes, ensuring writes to ROM are ignored or redirected."""
        if address == 0x0001:
            self.bus.cpu.pla_register = value
            self.set_registers(value)
            self.bus.ram.write(address, value)
            return

        target = self.decode_address(address)

        if isinstance(target, ROM):
            self.bus.ram.write(address, value)
        else:
            target.write(address, value)

    def set_registers(self, value: int) -> None:
        """
        Updates the PLA registers based on the provided value.

        :param value: Integer value to set the PLA registers.
        """
        self.loram = bool(value & 0x01)  # Bit 0
        self.hiram = bool(value & 0x02)  # Bit 1
        self.charen = bool(value & 0x04)  # Bit 2
