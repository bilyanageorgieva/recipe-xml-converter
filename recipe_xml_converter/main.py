from pathlib import Path

import click

from recipe_xml_converter.helpers import get_files_in_path, setup_logging
from recipe_xml_converter.orchestrator import RecipeOrchestrator

setup_logging()


@click.command
@click.option("--recipes", help="Full path to the RecipeML files.")
@click.option("--target", help="Full path where to save the transformed recipes.")
@click.option(
    "--max_files_combined",
    help="The maximum number of files to combine together.",
    default=1000,
)
def transform_and_save(recipes: str, target: str, max_files_combined: int) -> None:
    """
    Convert a RecipeML file to a MyCookbook XML one and save it to the file system.

    :param recipes: the full path to the RecipeML file or a directory containing RecipeML files
    :param target: the full path to the directory where the transformed recipes should be saved
    :param max_files_combined: the maximum number of files to combine together.
    """
    recipe_paths = get_files_in_path(Path(recipes))
    RecipeOrchestrator(recipe_paths, Path(target), max_files_combined).orchestrate()


if __name__ == "__main__":
    transform_and_save()
