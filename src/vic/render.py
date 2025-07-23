import numpy as np
import pygame

from src.bus.bus import Bus
from src.utils.log_setup import log

from .color.color import COLORS
from .registers_map import (
    MemorySetupRegister,
    ScreenControlRegister1,
    ScreenControlRegister2,
)


class Render:
    """Handles rendering of the C64 display, including character and sprite graphics."""

    def __init__(self, bus: Bus) -> None:
        """Initializes the rendering engine."""
        self.bus: Bus = bus
        self.screen_control_1: ScreenControlRegister1 = ScreenControlRegister1(bus)
        self.screen_control_2: ScreenControlRegister2 = ScreenControlRegister2(bus)
        self.memory_setup_register: MemorySetupRegister = MemorySetupRegister(bus)

        self.inner_width: int = 320
        self.inner_height: int = 200
        self.native_width: int = 403  # Full width (with borders)
        self.native_height: int = 312  # Full height (with borders)
        self.scale_factor: int = 3

        self.window_width: int = self.native_width * self.scale_factor
        self.window_height: int = self.native_height * self.scale_factor

        self.inner_x_start: int = (self.native_width - self.inner_width) // 2
        self.inner_y_start: int = (self.native_height - self.inner_height) // 2

        self.window: pygame.Surface = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )

        self.framebuffer: np.ndarray = np.zeros(
            (self.native_width, self.native_height), dtype=np.uint8
        )
        self.rgb_framebuffer: np.ndarray = np.zeros(
            (self.native_width, self.native_height, 3), dtype=np.uint8
        )
        self.color_base: int = 0xD800
        self.sprite_pixels: set[tuple[int, int]] = set()
        log.info(
            f"Render initialized with resolution: {self.window_width}, {self.window_height}"
        )

    def vic_bank(self) -> np.uint16:
        """Determines the active VIC-II memory bank."""
        vic_bank: int = (
            self.bus.cia_2.read(0xDD00) & 0x03
        ) ^ 0x03  # Bit order inversion
        return np.uint16(vic_bank) * 0x4000

    def read_chargen_via_vic(self, address: np.uint16) -> int:
        """Reads character generator data via VIC-II."""
        real_address: int = self.vic_bank() + (address & 0x3FFF)
        if 0x1000 <= (address & 0x3FFF) < 0x2000:
            return self.bus.chargen_rom.read(address)
        return self.bus.ram.read(real_address)

    def draw_frame(self) -> None:
        """Renders a single frame of the C64 display."""
        if not self.screen_control_1.screen_on:
            return

        border_color: np.uint8 = self.bus.vic.registers[0x20] & 0x0F
        background_color: np.uint8 = self.bus.vic.registers[0x21] & 0x0F

        num_col: int = self.screen_control_2.screen_width
        num_row: int = self.screen_control_1.screen_height

        self.framebuffer.fill(border_color)
        self.framebuffer[
            self.inner_x_start : self.inner_x_start + self.inner_width,
            self.inner_y_start : self.inner_y_start + self.inner_height,
        ] = background_color

        screen_mem_offset: np.uint16 = (
            self.memory_setup_register.screen_memory_pointer + self.vic_bank()
        )
        screen_size: int = num_col * num_row
        color_data: np.ndarray = self.bus.color_ram.data[0:screen_size] & 0x0F
        screen_data: np.ndarray = self.bus.ram.data[
            screen_mem_offset : screen_mem_offset + screen_size
        ]

        for row in range(num_row):
            for col in range(num_col):
                i: int = row * num_col + col
                char_code: np.uint16 = screen_data[i].astype(np.uint16)
                char_color: np.uint8 = color_data[i]

                for bit_row in range(8):
                    char_address: int = (
                        (char_code * 8)
                        + bit_row
                        + self.memory_setup_register.character_memory_pointer
                    )
                    bitmap: int = self.read_chargen_via_vic(char_address)

                    for bit_col in range(8):
                        pixel_x: int = col * 8 + bit_col + self.inner_x_start
                        pixel_y: int = row * 8 + bit_row + self.inner_y_start

                        if bitmap & (1 << (7 - bit_col)):
                            self.framebuffer[pixel_x, pixel_y] = char_color

        self.draw_sprites()
        self.update_pygame_display()

    def draw_sprites(self) -> None:
        """Draws sprites on the framebuffer and handles collision detection."""
        self.sprite_collision_mask: int = 0
        self.sprite_bg_collision_mask: int = 0

        for sprite_idx in range(8):
            sprite_enabled: int = self.bus.vic.registers[0x15] & (1 << sprite_idx)

            if not sprite_enabled:
                continue

            x_pos: np.uint8 = self.bus.vic.registers[0x00 + sprite_idx * 2]
            y_pos: np.uint8 = self.bus.vic.registers[0x01 + sprite_idx * 2]

            x_msb: np.uint8 = self.bus.vic.registers[0x10] & (1 << sprite_idx)
            if x_msb:
                x_pos += 256

            screen_mem_offset: int = (
                self.memory_setup_register.screen_memory_pointer + self.vic_bank()
            )

            sprite_pointer: np.uint8 = self.bus.read(
                screen_mem_offset + 0x3F8 + sprite_idx
            )
            sprite_address: np.uint16 = (int(sprite_pointer) * 64) + self.vic_bank()
            sprite_color: np.uint8 = self.bus.vic.registers[0x27 + sprite_idx] & 0x0F
            expand_x: np.uint8 = self.bus.vic.registers[0x1D] & (1 << sprite_idx)
            expand_y: np.uint8 = self.bus.vic.registers[0x17] & (1 << sprite_idx)
            scale_x: int = 2 if expand_x else 1
            scale_y: int = 2 if expand_y else 1
            sprite_behind_bg: np.uint8 = self.bus.vic.registers[0x1B] & (
                1 << sprite_idx
            )

            for row in range(21):
                sprite_data1: np.uint8 = self.read_chargen_via_vic(
                    sprite_address + row * 3
                )
                sprite_data2: np.uint8 = self.read_chargen_via_vic(
                    sprite_address + row * 3 + 1
                )
                sprite_data3: np.uint16 = self.read_chargen_via_vic(
                    sprite_address + row * 3 + 2
                )

                for col in range(24):
                    pixel_on: bool = bool(
                        sprite_data1 & (1 << (7 - col))
                        if col < 8
                        else (
                            sprite_data2 & (1 << (15 - col))
                            if col < 16
                            else sprite_data3 & (1 << (23 - col))
                        )
                    )

                    if pixel_on:
                        for dx in range(scale_x):
                            for dy in range(scale_y):
                                pixel_x: int = int(x_pos) + col * scale_x + dx
                                pixel_y: int = int(y_pos) + row * scale_y + dy

                                if (0 <= pixel_x < self.native_width) and (
                                    0 <= pixel_y < self.native_height
                                ):
                                    if (pixel_x, pixel_y) in self.sprite_pixels:
                                        self.sprite_collision_mask |= 1 << sprite_idx

                                    self.sprite_pixels.add((pixel_x, pixel_y))
                                    if (
                                        sprite_behind_bg
                                        and self.framebuffer[pixel_x, pixel_y] != 0
                                    ):
                                        self.sprite_bg_collision_mask |= 1 << sprite_idx
                                    else:
                                        self.framebuffer[pixel_x, pixel_y] = (
                                            sprite_color
                                        )

        self.bus.write(0xD01E, self.sprite_collision_mask)
        self.bus.write(0xD01F, self.sprite_bg_collision_mask)

    def update_pygame_display(self) -> None:
        """Updates the Pygame window with the rendered frame."""
        for y in range(self.native_height):
            for x in range(self.native_width):
                self.rgb_framebuffer[x, y] = COLORS[self.framebuffer[x, y]]

        surface: pygame.Surface = pygame.surfarray.make_surface(self.rgb_framebuffer)
        scaled_surface: pygame.Surface = pygame.transform.scale(
            surface, (self.window_width, self.window_height)
        )
        self.window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
