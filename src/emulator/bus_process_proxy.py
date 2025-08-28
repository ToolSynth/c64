import multiprocessing as mp
from dataclasses import dataclass
from multiprocessing.queues import Queue

from src.bus.bus import Bus
from src.utils.log_setup import log


@dataclass
class FrameQueue:
    """A container for passing the Bus instance between processes."""

    bus: Bus | None = None


class BusProcess(mp.Process):
    def __init__(self, queue: Queue) -> None:
        """
        A separate process for managing the Bus.

        :param queue: A multiprocessing queue to exchange data between processes.
        """
        super().__init__()
        # multiprocessing processes do not share normal attributes.  A simple
        # boolean flag would only change in the parent process and the child
        # would never notice the stop request.  Using an ``Event`` allows both
        # processes to share a synchronised flag.
        self.running: mp.Event = mp.Event()
        self.running.set()
        self.queue: Queue = queue

    def run(self) -> None:
        """Main execution loop for the bus process."""
        self.bus: Bus = Bus()
        self.queue.put(FrameQueue(bus=self.bus))

        while self.running.is_set():
            self.bus.cpu.execute_next_instruction()
            self.bus.vic.tick()
            self.bus.cia_1.tick()
            self.bus.cia_2.tick()
            self.bus.sid.tick()


class BusProcessProxy:
    def __init__(self) -> None:
        """Proxy class to manage the Bus process."""
        self.queue: mp.Queue = mp.Queue()
        self.bus_process: BusProcess = BusProcess(self.queue)
        self._bus: Bus | None = None
        self._running: bool = False

    def init_bus(self) -> None:
        """Starts the Bus process and initializes communication."""
        self.bus_process.start()
        self._running = True

        frame: FrameQueue = self.queue.get()
        if frame.bus is not None:
            self._bus = frame.bus
        log.info("[BusProcessProxy] Bus initialized, VIC and RAM received from child.")

    @property
    def is_running(self) -> bool:
        """Indicates whether the Bus process is currently running."""
        return self._running

    @property
    def bus(self) -> Bus:
        """Provides access to the Bus instance."""
        if self._bus is None:
            raise RuntimeError("Bus is not initialized.")
        return self._bus

    def stop(self) -> None:
        """Stops the Bus process if it is running."""
        if self._running:
            log.info("[BusProcessProxy] Running...")
            # Signal the child process to exit and wait for it to finish.
            self.bus_process.running.clear()
            self.bus_process.join()
            self._running = False
            log.info("[BusProcessProxy] BusProcess stopped.")

    def __del__(self) -> None:
        """Ensures the Bus process is stopped when the proxy is destroyed."""
        self.stop()
