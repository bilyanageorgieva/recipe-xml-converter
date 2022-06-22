import logging
from pathlib import Path
from typing import Union

from lxml import etree as ET

logger = logging.getLogger(__name__)


def convert_recipe(dom: ET._ElementTree) -> ET._XSLTResultTree:
    """
    Transform a RecipeML file using the stylesheet and return the result.

    :param dom: the parsed RecipeML file represented as a DOM tree
    :return: the result from the transformation represented as a tree
    """
    # TODO: fix types
    xslt = ET.parse(Path(__file__).parent.parent / "data/recipe.xsl")
    transform = ET.XSLT(xslt)
    new_dom = transform(dom)
    return new_dom


def convert_recipe_from_file(path: Union[Path, str]) -> ET._XSLTResultTree:
    """
    Transform a RecipeML file to a tree representation in the MyCookbook schema.

    :param path: the path to the RecipeML file
    :return: the result from the transformation represented as a tree
    """
    dom = ET.parse(path)
    return convert_recipe(dom)


def main() -> None:
    """Grab the RecipeML recipe, transform it to MyCookbook XML, and store it on the file system."""
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%H:%M:%S",
        format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    )

    recipe_path = Path(__file__).parent.parent / "data/'9os_Style_Chicken_Salad.xml"
    try:
        logger.info(f"Transforming recipe {recipe_path}")
        recipe = convert_recipe_from_file(recipe_path)
    except:
        logger.exception(f"Failed to transform recipe {recipe_path}")
    else:
        target_path = Path(__file__).parent.parent / "data/tranformed.xml"
        logger.info(f"✅ Recipe {recipe_path} transformed. Saving to file {target_path}")
        with open(target_path, "wb") as file:
            file.write(ET.tostring(recipe, pretty_print=True))


if __name__ == "__main__":
    main()
