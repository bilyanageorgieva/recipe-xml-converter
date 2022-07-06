import logging


def setup_logging() -> None:
    """Set up the common logging utilities."""
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%H:%M:%S",
        format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    )
