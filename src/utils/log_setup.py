import argparse
import logging


def setup_logging() -> logging.Logger:
    """
    Configures global logging for the Commodore 64 Emulator.

    :return: Configured logger instance.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Commodore 64 Emulator Logging Setup"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enables debug mode with more detailed logs",
    )
    args, _ = parser.parse_known_args()

    debug_enabled: bool = args.debug
    level: int = logging.DEBUG if debug_enabled else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger: logging.Logger = logging.getLogger("C64Emulator")
    logger.info("Logging configured")

    return logger


log: logging.Logger = setup_logging()
