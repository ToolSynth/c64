from collections import deque

from src.bus.memory.ram import RAM
from src.utils.log_setup import log


class KeyboardKernelBuffer:
    def __init__(self, ram: RAM, buffer_size: int = 10) -> None:
        """Manages the keyboard buffer in kernel memory."""
        self.ram: RAM = ram
        self.key_buffer: deque[int] = deque(maxlen=buffer_size)
        self.buffer_size: int = buffer_size
        log.debug(f"KeyboardKernelBuffer initialized with buffer size {buffer_size}")

    def add_to_buffer(self, key: int) -> None:
        """Adds a key to the memory buffer."""
        self.key_buffer.append(key)
        log.debug(f"Key added to buffer: {key}")

    def process_buffer(self) -> None:
        """Processes the contents of the memory buffer."""
        while self.key_buffer:
            key: int = self.key_buffer.popleft()
            log.debug(f"Processing key from buffer: {key}")
            self._write_to_kernel_buffer(key)

    def _write_to_kernel_buffer(self, key: int) -> None:
        """Handles writing the key to the kernel buffer."""
        ram_start: int = 0x0277
        status_reg: int = 0xC6

        if self.ram.read(ram_start) == 0x00:
            self.ram.write(ram_start, key)
            self.ram.write(status_reg, 0x1)
            log.debug(f"Key written directly to kernel buffer: {key}")
        else:
            buffer = self.ram.read_range(ram_start, ram_start + 9)
            try:
                index: int = buffer.index(0)  # Find the first free space in the buffer
                self.ram.write(ram_start + index, key)
                self.ram.write(status_reg, index + 1)
                log.debug(f"Key written to kernel buffer at index {index}: {key}")
            except ValueError:
                log.warning(f"Kernel buffer is full, key not written: {key}")
