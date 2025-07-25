from typing import TYPE_CHECKING

import pygame

from src.io_hw.keyboard.keyboard import KeyboardKernelInterface
from src.io_hw.loader_prg import BasicPrgLoader
from src.utils.log_setup import log
from src.vic.render import Render

if TYPE_CHECKING:
    from src.emulator.emulator import C64Emulator


class PygameInit:
    def __init__(self, emulator: "C64Emulator") -> None:
        """Initializes the Pygame interface for the C64 emulator."""
        self.emulator: C64Emulator = emulator
        self.keyboard_interface: KeyboardKernelInterface = KeyboardKernelInterface(
            emulator
        )
        self.render: Render = Render(bus=emulator.proxy.bus)
        self.loader_prg: BasicPrgLoader = BasicPrgLoader(emulator.proxy.bus.ram)
        self.global_clock: pygame.time.Clock = pygame.time.Clock()

    def run(self) -> None:
        """Initializes Pygame and starts the main event loop."""
        pygame.init()
        pygame.display.set_caption("C64 Emulator")
        self._main_loop()

    def _main_loop(self) -> None:
        """Handles the main event loop for user input and rendering."""
        while self.emulator.proxy.is_running:
            key_events = pygame.event.get()
            for event in key_events:
                if event.type == pygame.QUIT:
                    self.emulator.proxy.stop()
                    log.debug("QUIT event detected, stopping emulator.")
                elif event.type == pygame.KEYDOWN:
                    log.debug(f"KEYDOWN event detected: {pygame.key.name(event.key)}")
                    self.keyboard_interface.scan_and_process(event)
                elif event.type == pygame.DROPFILE:
                    dropped_file: str = event.file
                    self.loader_prg.init_program(dropped_file)

            self.render.draw_frame()
            self.global_clock.tick(25)
