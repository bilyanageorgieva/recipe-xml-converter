from pathlib import Path
from typing import Union

from lxml import etree as ET


def convert_recipe(dom: ET._ElementTree) -> ET._XSLTResultTree:
    # TODO: fix types
    xslt = ET.parse(Path(__file__).parent.parent / "data/recipe.xsl")
    transform = ET.XSLT(xslt)
    new_dom = transform(dom)

    with open(Path(__file__).parent.parent / "data/tranformed.xml", "wb") as file:
        file.write(ET.tostring(new_dom, pretty_print=True))

    return new_dom


def convert_recipe_from_file(path: Union[Path, str]) -> ET._ElementTree:
    dom = ET.parse(path)
    return convert_recipe(dom)


if __name__ == "__main__":
    convert_recipe_from_file(
        Path(__file__).parent.parent / "data/'9os_Style_Chicken_Salad.xml"
    )
