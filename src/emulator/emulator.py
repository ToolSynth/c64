import pygame

from src.utils.log_setup import log

from .bus_process_proxy import BusProcessProxy
from .pygame_init import PygameInit


class C64Emulator:
    def __init__(self) -> None:
        """Initializes the C64 emulator."""
        self.basic_running: bool = False
        self.proxy: BusProcessProxy = BusProcessProxy()

    def reset(self) -> None:
        """Resets the emulator to its initial state."""
        raise NotImplementedError("Emulator reset not implemented")

    def run(self) -> None:
        """Starts the emulator and initializes the bus and Pygame interface."""
        try:
            self.proxy.init_bus()
            pygame_init: PygameInit = PygameInit(self)
            pygame_init.run()
        except KeyboardInterrupt:
            log.info("KeyboardInterrupt received. Stopping threads...")
        finally:
            self.proxy.stop()
            pygame.quit()
            log.info("Program terminated successfully.")

    def stop(self) -> None:
        """Stops the emulator execution."""
        raise NotImplementedError("Stop Emulator not implemented")

    def pause(self) -> None:
        """Pauses the emulator execution."""
        raise NotImplementedError("Pause Emulator not implemented")

    def save_state(self) -> None:
        """Saves the emulator state (e.g., to a file)."""
        raise NotImplementedError("Save state not implemented")

    def load_state(self) -> None:
        """Loads the emulator state (e.g., from a file)."""
        raise NotImplementedError("Load state not implemented")
