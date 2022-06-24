import logging
from pathlib import Path
from typing import Union

import click
from lxml import etree as ET

from recipe_xml_converter.helpers import setup_logging

logger = logging.getLogger(__name__)


TRANSFORM_XSLT = Path(__file__).parent.parent / "data/transform.xsl"
"""The path to the XSLT stylesheet used for the main transformation."""

NORMALIZE_SPACE_XSLT = Path(__file__).parent.parent / "data/normalize_space.xsl"
"""The path to the XSLT stylesheet used for the removal of extra spaces."""


def convert_recipe(dom: ET._ElementTree) -> ET._XSLTResultTree:
    """
    Transform a RecipeML file using the stylesheet and return the result.

    :param dom: the parsed RecipeML file represented as a DOM tree
    :return: the result from the transformation represented as a tree
    """
    transform = ET.XSLT(ET.parse(TRANSFORM_XSLT))
    normalize_space = ET.XSLT(ET.parse(NORMALIZE_SPACE_XSLT))
    new_dom = normalize_space(transform(dom))
    return new_dom


def convert_recipe_from_file(path: Union[Path, str]) -> ET._XSLTResultTree:
    """
    Transform a RecipeML file to a tree representation in the MyCookbook schema.

    :param path: the path to the RecipeML file
    :return: the result from the transformation represented as a tree
    """
    dom = ET.parse(path)
    return convert_recipe(dom)


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
    try:
        logger.info(f"Transforming recipe {recipe}")
        transformed = convert_recipe_from_file(recipe)
    except:
        logger.exception(f"Failed to transform recipe {recipe}")
    else:
        logger.info(f"✅ Recipe {recipe} transformed. Saving to file {target}")
        with open(target, "wb") as file:
            file.write(ET.tostring(transformed, pretty_print=True))


if __name__ == "__main__":
    convert_and_save_recipe_to_file()
