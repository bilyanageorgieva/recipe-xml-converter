from pathlib import Path

from decouple import config

BASE_DATA_DIR = config(
    "BASE_DATA_DIR", default=str(Path(__file__).parent.parent / "data")
)
DEBUG = config("DEBUG", default=False)
