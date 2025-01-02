from pathlib import PurePath

import numpy as np

from src.bus.memory.color_ram import ColorRAM
from src.bus.memory.pla import PLA
from src.bus.memory.ram import RAM
from src.bus.memory.rom import ROM
from src.cia.cia_1 import CIA1
from src.cia.cia_2 import CIA2
from src.cpu.cpu import CPU
from src.sid.sid import SID
from src.utils.log_setup import log
from src.vic.vic import VIC

path: PurePath = PurePath(__file__).parent.parent.parent.joinpath("rom")


class Bus:
    def __init__(self) -> None:
        log.info("Bus Initializing Components...")
        self.kernel_rom: ROM = ROM(
            filepath=path.joinpath("kernel.bin"),
            size=8192,
            start_address=0xE000,
        )
        self.basic_rom: ROM = ROM(
            filepath=path.joinpath("basic.bin"), size=8192, start_address=0xA000
        )
        self.chargen_rom: ROM = ROM(
            filepath=path.joinpath("chargen.bin"),
            size=4096,
            start_address=0x1000,
        )
        self.pla: PLA = PLA(self)
        self.ram: RAM = RAM()
        self.color_ram: ColorRAM = ColorRAM()
        self.cpu: CPU = CPU(self)
        self.vic: VIC = VIC(self)
        self.sid: SID = SID(self)
        self.cia_1: CIA1 = CIA1(self)
        self.cia_2: CIA2 = CIA2(self)
        self.main_reset()
        log.info("Bus Initialized.")

    def main_reset(self) -> None:
        self.cpu.reset()
        self.ram.reset()

    def trigger_irq(self) -> None:
        self.cpu.handle_irq()

    def read(self, address: int) -> int | np.uint8:
        return self.pla.read(address)

    def write(self, address: int, value: int) -> None:
        self.pla.write(address, value)
