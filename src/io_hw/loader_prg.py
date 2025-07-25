from pathlib import Path

import numpy as np

from src.bus.memory.ram import RAM
from src.utils.log_setup import log


class BasicPrgLoader:
    """
    Loader for .PRG files. Ensures the program is correctly loaded into memory
    and configures the BASIC pointers to execute it.
    """

    def __init__(self, ram: RAM) -> None:
        """
        Initializes the loader with a reference to the emulator's RAM.

        :param ram: An object representing the emulator's RAM.
        """
        self.ram: RAM = ram

    def init_program(self, filepath: str) -> None:
        """
        Loads a .PRG file into memory and updates BASIC pointers.

        :param filepath: Path to the .PRG file to be loaded.
        :raises ValueError: If the file is too short or exceeds available memory.
        """
        with Path.open(filepath, "rb") as file:
            header: bytes = file.read(2)
            if len(header) < 2:
                raise ValueError("The .PRG file is too short.")

            load_address: int = header[0] + (header[1] << 8)
            log.info(f"Load address from header: {hex(load_address)}")

            file_content: bytes = file.read()
            file_size: int = len(file_content)

            ram_size: int = len(self.ram.data)
            if load_address + file_size > ram_size:
                raise ValueError("File exceeds available memory.")

            arr: np.ndarray = np.frombuffer(file_content, dtype=np.uint8)
            self.ram.data[load_address : load_address + file_size] = arr

            self.update_basic_pointers(load_address, load_address + file_size)

            log.info(
                f"Loaded '{filepath}' at {hex(load_address)}, size={file_size} "
                f"bytes, end address: {hex(load_address + file_size)}."
            )

    def update_basic_pointers(self, start_address: int, end_address: int) -> None:
        """
        Updates the BASIC pointers for the program.

        :param start_address: The start address of the program in memory.
        :param end_address: The end address of the program in memory.
        """
        # Start of BASIC program
        self.ram.data[0x002B] = start_address & 0xFF
        self.ram.data[0x002C] = (start_address >> 8) & 0xFF

        # End of BASIC program
        self.ram.data[0x002D] = end_address & 0xFF
        self.ram.data[0x002E] = (end_address >> 8) & 0xFF

        # Start of variables (right after the program)
        vars_address: int = end_address
        self.ram.data[0x0031] = vars_address & 0xFF
        self.ram.data[0x0032] = (vars_address >> 8) & 0xFF

        log.info(
            f"Updated BASIC pointers: start={hex(start_address)}, "
            f"end={hex(end_address)}, vars={hex(vars_address)}."
        )
