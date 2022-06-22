import pytest
from lxml.builder import E

from recipe_xml_converter.converter import convert_recipe


def test_correct_number_of_ingredients() -> None:
    """Assert the correct number of ingredients have been created."""
    ing_num = 5
    recipe_ml = E.recipeml(E.recipe(E.ingredients(*[E.ing() for _ in range(ing_num)])))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/ingredient/li")) == ing_num


@pytest.mark.parametrize(
    "ingredient_element,ingredient_text",
    [
        (E.ing(E.amt(E.qty("2"), E.unit()), E.item("apples")), "2 apples"),
        (E.ing(E.amt(E.qty("3")), E.item("oranges")), "3 oranges"),
        (E.ing(E.amt(E.qty("5"), E.unit("cups")), E.item("water")), "5 cups water"),
        (
            E.ing(
                E.amt(E.qty(E.frac(E.n("1"), E.d("2"))), E.unit("cup")), E.item("water")
            ),
            "1/2 cup water",
        ),
        (
            E.ing(
                E.amt(E.qty(E.range(E.q1("1"), E.q2("2"))), E.unit("cups")),
                E.item("water"),
            ),
            "1 - 2 cups water",
        ),
        (
            E.note(
                "About ",
                E.amt(E.qty("500"), E.unit("grams")),
                " of ",
                E.temp(E.qty("20"), E.tempunit("degree C")),
                " butter",
            ),
            "About 500 grams of 20 degree C butter",
        ),
    ],
)
def test_ingredient_is_correct(ingredient_element: E, ingredient_text: str) -> None:
    """Assert the ingredients have the right values."""
    recipe_ml = E.recipeml(E.recipe(E.ingredients(ingredient_element)))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert my_cookbook_xml.xpath("recipe/ingredient/li")[0].text == ingredient_text
