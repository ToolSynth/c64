from src.emulator.emulator import C64Emulator
from src.utils.log_setup import log


def main() -> None:
    emulator = C64Emulator()

    try:
        emulator.run()
    except KeyboardInterrupt:
        log.info("Emulator zakończony przez użytkownika.")


if __name__ == "__main__":
    main()
