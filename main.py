import argparse

from src.emulator.emulator import C64Emulator
from src.utils.log_setup import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Commodore 64 Emulator")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with more detailed logs",
    )
    args = parser.parse_args()

    log = setup_logging(debug=args.debug)
    emulator = C64Emulator()

    try:
        emulator.run()
    except KeyboardInterrupt:
        log.info("Emulator terminated by user.")


if __name__ == "__main__":
    main()
