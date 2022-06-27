import pytest
from lxml.builder import E

from recipe_xml_converter.transformer import RecipeTransformer
from tests.fixtures import transformer  # noqa: F401


@pytest.mark.parametrize(
    "recipeml,mycookbook",
    [
        (
            (
                E.recipe(E.head(E.title("Recipe 1"))),
                E.recipe(E.head(E.title("Recipe 2"))),
            ),
            (E.recipe(E.title("Recipe 1")), E.recipe(E.title("Recipe 2"))),
        ),
    ],
)
def test_menu_is_parsed_correctly(
    transformer: RecipeTransformer, recipeml: tuple[E, ...], mycookbook: tuple[E, ...]
):
    """Assert the menu element is parsed correctly."""
    dom = E.recipeml(E.menu(*recipeml))
    dom = transformer._transform(dom)
    recipe_elements = dom.xpath("recipe")
    assert len(recipe_elements) == len(mycookbook)
    for i in range(len(recipe_elements)):
        assert (
            recipe_elements[i].xpath("title")[0].text
            == mycookbook[i].xpath("title")[0].text
        )
