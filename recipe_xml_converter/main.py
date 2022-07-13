import logging
import tempfile
from pathlib import Path

import click
from fastapi import BackgroundTasks, FastAPI, Form, UploadFile
from fastapi.responses import FileResponse

from recipe_xml_converter import config
from recipe_xml_converter.helpers import (
    get_files_in_path,
    remove_temp_dir,
    setup_logging,
)
from recipe_xml_converter.orchestrator import RecipeOrchestrator

app = FastAPI()
"""The FastAPI app to use for the HTTP requests."""

setup_logging()

logger = logging.getLogger(__name__)


@click.command
@click.option(
    "--recipes",
    "-r",
    multiple=True,
    help="Full paths to the RecipeML files or folders.",
)
@click.option(
    "--target", "-t", help="Full path to the directory to save the transformed recipes."
)
@click.option(
    "--max_files_combined",
    help="The maximum number of files to combine together.",
    default=1000,
)
def transform_and_save(
    recipes: tuple[str, ...], target: str, max_files_combined: int
) -> None:
    """
    Convert RecipeML files to MyCookbook XML ones and save them as a zip to the file system.

    :param recipes: the full paths to the RecipeML files or a directories
    :param target: the full path to the directory where the transformed recipes should be saved
    :param max_files_combined: the maximum number of files to combine together.
    """
    recipe_paths = tuple(
        [path for paths in recipes for path in get_files_in_path(Path(paths))]
    )
    orchestrator = RecipeOrchestrator(recipe_paths, Path(target), max_files_combined)
    archive_path = orchestrator.orchestrate()
    logger.info(f"✅ Saved transformed recipes to {archive_path}")


@app.post("/transform/")
async def transform_recipes(
    files: list[UploadFile],
    background_tasks: BackgroundTasks,
    max_combined_files: int = Form(),
) -> FileResponse:
    """
    Transform RecipeML files to MyCookbook XML ones and return a zip containing the results.

    :param files: the RecipeML files
    :param background_tasks: tasks to run after the response is returned
    :param max_combined_files: the maximum number of files to combine in one
    :return: a zip file containing all the transformed MyCookbook XML files
    """
    temp_dir = tempfile.TemporaryDirectory(dir=config.BASE_DATA_DIR)
    background_tasks.add_task(remove_temp_dir, temp_dir)

    orchestrator = RecipeOrchestrator(
        tuple([f.file for f in files]), Path(temp_dir.name), max_combined_files
    )
    return FileResponse(orchestrator.orchestrate())


if __name__ == "__main__":
    transform_and_save()
