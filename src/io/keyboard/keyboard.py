from typing import TYPE_CHECKING

import pygame

from src.bus.memory.keyboard_buffer import KeyboardKernelBuffer
from src.utils.log_setup import log

from .matrix import c64_keymap

if TYPE_CHECKING:
    from src.emulator.emulator import C64Emulator


class Keyboard:
    def __init__(
        self, kernel_buffer: KeyboardKernelBuffer, emulator: "C64Emulator"
    ) -> None:
        """Initializes the keyboard handling for the C64 emulator."""
        self.kernel_buffer: KeyboardKernelBuffer = kernel_buffer
        self.emulator: C64Emulator = emulator
        log.debug("Keyboard initialized")

    def handle_keydown(self, event: pygame.event.Event) -> None:
        """Handles keydown events."""
        key_name: str = pygame.key.name(event.key)
        key_value: int | None = self._map_key(event, key_name)

        if key_value is not None:
            log.debug(f"Mapped key: {key_name} to value: {key_value}")
            self.kernel_buffer.add_to_buffer(key_value)
        else:
            log.debug(f"Key not mapped: {key_name}")

    def _map_key(self, event: pygame.event.Event, key_name: str) -> int | None:
        """Maps a key to a C64 keyboard value."""
        if event.unicode and (event.mod & pygame.KMOD_SHIFT):
            return c64_keymap.get(event.unicode)

        if not (event.mod & pygame.KMOD_SHIFT):
            return c64_keymap.get(key_name)

        return None


class KeyboardKernelInterface:
    def __init__(self, emulator: "C64Emulator", buffer_size: int = 10) -> None:
        """Initializes the keyboard kernel interface."""
        self.kernel_buffer: KeyboardKernelBuffer = KeyboardKernelBuffer(
            emulator.proxy.bus.ram, buffer_size
        )
        self.keyboard: Keyboard = Keyboard(self.kernel_buffer, emulator)

    def scan_and_process(self, event: pygame.event.Event) -> None:
        """Scans the keyboard and processes the buffer."""
        self.keyboard.handle_keydown(event)
        self.kernel_buffer.process_buffer()
