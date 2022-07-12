import logging
from pathlib import Path


def setup_logging() -> None:
    """Set up the common logging utilities."""
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%H:%M:%S",
        format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    )


def get_files_in_path(path: Path) -> tuple[Path, ...]:
    if path.is_file():
        return (path,)
    elif path.is_dir():
        return tuple(path.rglob("*.xml"))
    else:
        raise ValueError(f"Cannot locate input file(s) at {path}")
