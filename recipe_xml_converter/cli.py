import logging
from pathlib import Path

import click

from recipe_xml_converter.helpers import get_files_in_path, setup_logging
from recipe_xml_converter.orchestrator import RecipeOrchestrator

setup_logging()

logger = logging.getLogger(__name__)


@click.command
@click.option(
    "--recipes",
    "-r",
    multiple=True,
    help="Full paths to the RecipeML files or folders that should be transformed.",
)
@click.option(
    "--target", "-t", help="Full path to the directory to save the transformed files."
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


if __name__ == "__main__":
    transform_and_save()
