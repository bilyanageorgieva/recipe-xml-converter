import logging
import tempfile
from pathlib import Path

from recipe_xml_converter import config


def setup_logging() -> None:
    """Set up the common logging utilities."""
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        datefmt="%H:%M:%S",
        format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    )


def get_files_in_path(path: Path) -> tuple[Path, ...]:
    """
    Return all the files contained in the path.

    :param path: the path to traverse
    :return: the paths to all files contained in the path
    """
    if path.is_file():
        return (path,)
    elif path.is_dir():
        return tuple(path.rglob("*.xml"))
    else:
        raise ValueError(f"Cannot locate input file(s) at {path}")


def remove_temp_dir(temp_dir: tempfile.TemporaryDirectory) -> None:
    """Cleanup the temporary directory."""
    temp_dir.cleanup()
