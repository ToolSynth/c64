from enum import Enum

from src.bus.bus import Bus


class BitmapMode(str, Enum):
    """Represents the bitmap and text modes of the C64 screen."""

    bitmap = "bitmap_mode"
    text = "text_mode"


class ScreenControlRegister1:
    """Screen Control Register #1 (0xD011)"""

    def __init__(self, bus: Bus) -> None:
        """Initializes the Screen Control Register #1."""
        self.bus: Bus = bus

    def read_register(self) -> int:
        """Reads the entire value of register 0xD011."""
        return int(self.bus.vic.read(0xD011))

    @property
    def vertical_raster_scroll(self) -> int:
        """Bits 0-2: Vertical raster scroll."""
        return self.read_register() & 0b00000111  # Bits 0-2

    @property
    def screen_height(self) -> int:
        """Bit 3: Screen height (0=24 rows, 1=25 rows)."""
        return 25 if (self.read_register() >> 3) & 1 else 24

    @property
    def screen_on(self) -> bool:
        """Bit 4: Screen enabled."""
        return bool((self.read_register() >> 4) & 1)

    @property
    def bitmap_mode(self) -> BitmapMode:
        """Bit 5: Bitmap mode enabled or text mode."""
        return BitmapMode.bitmap if (self.read_register() >> 5) & 1 else BitmapMode.text

    @property
    def extended_background_mode(self) -> bool:
        """Bit 6: Extended background mode."""
        return bool((self.read_register() >> 6) & 1)

    @property
    def raster_interrupt_bit(self) -> int:
        """Bit 7: Current raster line (bit #8)."""
        return (self.read_register() >> 7) & 1

    def __repr__(self) -> str:
        """Returns a detailed representation of the register and its values."""
        return (
            f"ScreenControlRegister1 (0xD011)\n"
            f"---------------------------------\n"
            f"Register Value (bin)  : {self.read_register():08b}\n"
            f"Vertical Raster Scroll: {self.vertical_raster_scroll}\n"
            f"Screen Height         : {self.screen_height}\n"
            f"Screen On             : {self.screen_on}\n"
            f"Bitmap Mode           : {self.bitmap_mode}\n"
            f"Extended Background   : {self.extended_background_mode}\n"
            f"Raster Interrupt Bit  : {self.raster_interrupt_bit}"
        )


class ScreenControlRegister2:
    """Screen Control Register #2 (0xD016)"""

    def __init__(self, bus: Bus) -> None:
        """Initializes the Screen Control Register #2."""
        self.bus: Bus = bus

    def read_register(self) -> int:
        """Reads the entire value of register 0xD016."""
        return int(self.bus.vic.read(0xD016))

    @property
    def horizontal_raster_scroll(self) -> int:
        """Bits 0-2: Horizontal raster scroll."""
        return self.read_register() & 0b00000111  # Bits 0-2

    @property
    def screen_width(self) -> int:
        """Bit 3: Screen width (0=38 columns, 1=40 columns)."""
        return 40 if (self.read_register() >> 3) & 1 else 38

    @property
    def multicolor_mode(self) -> bool:
        """Bit 4: Multicolor mode enabled."""
        return bool((self.read_register() >> 4) & 1)

    def __repr__(self) -> str:
        """Returns a detailed representation of the register and its values."""
        return (
            f"ScreenControlRegister2 (0xD016)\n"
            f"---------------------------------\n"
            f"Register Value (bin)  : {self.read_register():08b}\n"
            f"Horizontal Raster Scroll: {self.horizontal_raster_scroll}\n"
            f"Screen Width          : {self.screen_width}\n"
            f"Multicolor Mode       : {self.multicolor_mode}"
        )


class MemorySetupRegister:
    """VIC-II Memory Configuration Register (0xD018)"""

    def __init__(self, bus: Bus) -> None:
        """Initializes the VIC-II memory setup register."""
        self.bus: Bus = bus

    def read_register(self) -> int:
        """Reads the entire value of register 0xD018."""
        return int(self.bus.vic.read(0xD018))

    @property
    def character_memory_pointer(self) -> int:
        """Computes the actual character memory address."""
        char_ptr: int = (self.read_register() >> 1) & 0b00000111  # Bits 1-3
        return 0x0800 * char_ptr  # Converts to actual address

    @property
    def bitmap_memory_pointer(self) -> int:
        """Computes the actual bitmap memory address."""
        bitmap_ptr: int = (
            self.character_memory_pointer >> 2
        ) & 1  # Bits 2-3 determine bitmap
        return 0x2000 if bitmap_ptr else 0x0000  # 0x0000 for %0xx, 0x2000 for %1xx

    @property
    def screen_memory_pointer(self) -> int:
        """Computes the actual screen memory address."""
        screen_ptr: int = self.read_register() >> 4  # Bits 4-7 determine screen memory
        return screen_ptr * 0x400  # Converts to actual address

    def __repr__(self) -> str:
        """Returns a detailed representation of the register and its values."""
        return (
            f"MemorySetupRegister (0xD018)\n"
            f"---------------------------------\n"
            f"Register Value (bin)/(hex)  : {self.read_register():08b}/{hex(self.read_register())}\n"
            f"Character Memory Addr : {hex(self.character_memory_pointer)}\n"
            f"Bitmap Memory Addr    : {hex(self.bitmap_memory_pointer)}\n"
            f"Screen Memory Addr    : {hex(self.screen_memory_pointer)}"
        )
