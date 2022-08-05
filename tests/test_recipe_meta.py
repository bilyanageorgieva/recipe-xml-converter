import pytest
from lxml.builder import E

from recipe_xml_converter.transformer import RecipeTransformer
from tests.fixtures import transformer  # noqa: F401


@pytest.mark.parametrize(
    "element_name",
    [
        "DC.Creator",
        "DC.Source",
        "DC.Identifier",
        "DC.Publisher",
        "DC.Date",
        "DC.Rights",
    ],
)
def test_source_meta_element_exists(
    transformer: RecipeTransformer, element_name: str
) -> None:
    """Assert the meta element exists within the source tag."""
    recipe_ml = E.recipeml(E("meta", name=element_name, content=""), E.recipe())
    my_cookbook_xml = transformer._transform(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/source/li")) == 1


@pytest.mark.parametrize(
    "element_name,element_value",
    [
        ("DC.Creator", "Creator Name"),
        ("DC.Source", "Some Source Value"),
        ("DC.Identifier", "The right identifier"),
        ("DC.Publisher", "The publishing house"),
        ("DC.Date", "12.01.2000"),
        ("DC.Rights", "Copyright 1958"),
    ],
)
def test_source_meta_element_is_correct(
    transformer: RecipeTransformer, element_name: str, element_value: str
) -> None:
    """Assert the meta element is correctly transformed within the source tag."""
    recipe_ml = E.recipeml(
        E("meta", name=element_name, content=element_value), E.recipe()
    )
    my_cookbook_xml = transformer._transform(recipe_ml)
    assert (
        my_cookbook_xml.xpath("recipe/source/li")[0].text
        == f"{element_name[3:]}: {element_value}"
    )


def test_source_meta_elements_exist_together(transformer: RecipeTransformer) -> None:
    """Assert that multiple source elements exist together within a single source element in the target doc."""
    meta_el = {
        "DC.Creator": "Creator Name",
        "DC.Source": "Source Name",
        "DC.Identifier": "ID Name",
        "DC.Publisher": "Publisher Name",
        "DC.Date": "12.01.2000",
        "DC.Rights": "Copyright 1958",
    }
    recipe_ml = E.recipeml(
        *[E("meta", name=name, content=content) for name, content in meta_el.items()],
        E.recipe(),
    )
    my_cookbook_xml = transformer._transform(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/source")) == 1
    assert len(my_cookbook_xml.xpath("recipe/source/li")) == len(meta_el)


def test_source_meta_elements_are_correct(transformer: RecipeTransformer) -> None:
    """Assert that when the creator and source elements are both present, their transformed values are correct."""
    meta_el = {
        "DC.Creator": "Creator Name",
        "DC.Source": "Source Name",
        "DC.Identifier": "ID Name",
        "DC.Publisher": "Publisher Name",
        "DC.Date": "12.01.2000",
        "DC.Rights": "Copyright 1958",
    }
    recipe_ml = E.recipeml(
        *[E("meta", name=name, content=content) for name, content in meta_el.items()],
        E.recipe(),
    )
    my_cookbook_xml = transformer._transform(recipe_ml)
    source_elements = my_cookbook_xml.xpath("recipe/source/li")
    assert len(source_elements) == len(meta_el)

    for i, el in enumerate(meta_el.items()):
        name, content = el
        assert source_elements[i].text == f"{name[3:]}: {content}"
