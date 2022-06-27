import click

from recipe_xml_converter.helpers import setup_logging
from recipe_xml_converter.transformer import RecipeTransformer


@click.command
@click.option("--recipe", help="Full path to the RecipeML file.")
@click.option("--target", help="Full path where to save the transformed recipe.")
def convert_and_save_recipe_to_file(recipe: str, target: str) -> None:
    """
    Convert a RecipeML file to a MyCookbook XML one and save it to the file system.

    :param recipe: the full path to the RecipeML file
    :param target: the full path where the transformed recipe should be saved
    """
    setup_logging()
    transformer = RecipeTransformer(recipe, target)
    transformer.transform_and_save()


if __name__ == "__main__":
    convert_and_save_recipe_to_file()
