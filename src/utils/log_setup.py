import logging

log: logging.Logger = logging.getLogger("C64Emulator")


def setup_logging(*, debug: bool = False) -> logging.Logger:
    """
    Configure global logging for the Commodore 64 Emulator.

    Parameters
    ----------
    debug: bool
        Enables debug mode with more detailed logs.

    Returns
    -------
    logging.Logger
        Configured logger instance.

    """
    level: int = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log.setLevel(level)
    log.info("Logging configured")

    return log
