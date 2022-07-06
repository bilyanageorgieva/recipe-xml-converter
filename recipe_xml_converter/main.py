import click

from recipe_xml_converter.helpers import setup_logging
from recipe_xml_converter.orchestrator import RecipeOrchestrator


@click.command
@click.option("--recipes", help="Full path to the RecipeML files.")
@click.option("--target", help="Full path where to save the transformed recipes.")
@click.option(
    "--max_files_combined",
    help="The maximum number of files to combine together.",
    default=1000,
)
def convert_and_save_to_file(
    recipes: str, target: str, max_files_combined: int
) -> None:
    """
    Convert a RecipeML file to a MyCookbook XML one and save it to the file system.

    :param recipes: the full path to the RecipeML file or a directory containing RecipeML files
    :param target: the full path to the directory where the transformed recipes should be saved
    :param max_files_combined: the maximum number of files to combine together.
    """
    setup_logging()
    RecipeOrchestrator(recipes, target, max_files_combined).transform()


if __name__ == "__main__":
    convert_and_save_to_file()
