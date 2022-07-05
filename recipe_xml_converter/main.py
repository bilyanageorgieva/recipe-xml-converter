import click

from recipe_xml_converter.helpers import setup_logging
from recipe_xml_converter.orchestrator import Orchestrator


@click.command
@click.option("--recipes", help="Full path to the RecipeML file.")
@click.option("--target", help="Full path where to save the transformed recipe.")
def convert_and_save_to_file(recipes: str, target: str) -> None:
    """
    Convert a RecipeML file to a MyCookbook XML one and save it to the file system.

    :param recipes: the full path to the RecipeML file or a folder containing RecipeML files
    :param target: the full path where the transformed recipes should be saved
    """
    setup_logging()
    orchestrator = Orchestrator(recipes, target)
    orchestrator.transform()


if __name__ == "__main__":
    convert_and_save_to_file()
