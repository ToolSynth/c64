from src.utils.log_setup import log


class Timer:
    def __init__(
        self, name: str = "Timer", mode: str = "PAL", irq_bit: int = 0
    ) -> None:
        self.name = name
        self.value = 0  # Current countdown value
        self.reload = 0  # Reload value
        self.running = False  # Operation status
        self.irq_bit = irq_bit  # Interrupt bit for this timer
        self.interrupt_triggered = False
        self._control_register = 0  # Stores control register state
        log.info(f"{self.name} initialized in {mode} mode.")

    def configure(
        self,
        *,
        low_byte: int | None = None,
        high_byte: int | None = None,
        force_load: bool = False,
        start: bool = False,
    ) -> None:
        if low_byte is not None:
            self.reload = (self.reload & 0xFF00) | low_byte
        if high_byte is not None:
            self.reload = (self.reload & 0x00FF) | (high_byte << 8)
        if force_load:
            self.value = self.reload
        self.running = start
        self.control_register = (0x10 if force_load else 0x00) | (
            0x01 if start else 0x00
        )
        log.debug(
            f"{self.name} configured: Reload={self.reload}, Force Load={force_load}, Start={self.running}"
        )

    def tick(self, cycles: int) -> None:
        if self.running:
            self.value -= cycles
            if self.value <= 0:
                self.value += self.reload
                self.interrupt_triggered = True
                log.debug(f"{self.name} expired and reloaded to {self.reload}.")

    def clear_interrupt(self) -> None:
        self.interrupt_triggered = False
        log.debug(f"{self.name} interrupt cleared.")

    @property
    def low_byte(self) -> int:
        return int(self.value) & 0xFF

    @property
    def high_byte(self) -> int:
        return (int(self.value) >> 8) & 0xFF

    @property
    def control_register(self) -> int:
        return self._control_register

    @control_register.setter
    def control_register(self, value: int) -> None:
        self.running = bool(value & 0x01)
        if value & 0x10:
            self.value = self.reload
        self._control_register = value & 0xFF
