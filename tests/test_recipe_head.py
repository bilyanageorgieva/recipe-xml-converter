from lxml import etree as ET
from lxml.builder import E

from recipe_xml_converter.converter import convert_recipe


def test_title_exists() -> None:
    """Assert the title element exists."""
    title = "Recipe Title"
    recipe_ml = E.recipeml(E.recipe(E.head(E.title(title))))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert my_cookbook_xml.xpath("recipe/title")


def test_title_exists_without_value() -> None:
    """Assert the title element exists even when the original title is missing."""
    recipe_ml = E.recipeml(E.recipe(E.head(E.title())))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert my_cookbook_xml.xpath("recipe/title")


def test_title_is_correct() -> None:
    """Assert the title has correct value."""
    title = "Recipe Title"
    recipe_ml = E.recipeml(E.recipe(E.head(E.title(title))))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert my_cookbook_xml.xpath("string(recipe/title)") == title
