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
        # basic ingredient
        (E.ing(E.amt(E.qty("2"), E.unit()), E.item("apples")), "2 apples"),
        (E.ing(E.amt(E.qty("3")), E.item("oranges")), "3 oranges"),
        (E.ing(E.amt(E.qty("5"), E.unit("cups")), E.item("water")), "5 cups water"),
        # fractions
        (
            E.ing(
                E.amt(E.qty(E.frac(E.n("1"), E.d("2"))), E.unit("cup")), E.item("water")
            ),
            "1/2 cup water",
        ),
        # range
        (
            E.ing(
                E.amt(E.qty(E.range(E.q1("1"), E.q2("2"))), E.unit("cups")),
                E.item("water"),
            ),
            "1 - 2 cups water",
        ),
        # size
        (
            E.ing(
                E.amt(
                    E.size(E.qty(E.frac(E.n("1"), E.d("2"))), E.unit("cup")),
                ),
                E.item("water"),
            ),
            "1/2 cup water",
        ),
        # size with text
        (
            E.ing(
                E.amt(
                    E.size("2/3 ", E.unit("cup")),
                ),
                E.item("water"),
            ),
            "2/3 cup water",
        ),
        (
            E.ing(
                E.amt(
                    E.size(E.range(E.q1("2"), E.q2("3")), E.unit("cups"), " warm"),
                ),
                E.item("water"),
            ),
            "2 - 3 cups warm water",
        ),
        # amt - everything combined
        (
            E.ing(
                E.amt(
                    E.qty(E.frac(E.n("1"), E.d("2"))),
                    E.size(E.range(E.q1("2"), E.q2("3")), E.unit("cups"), " warm"),
                    E.unit("cups"),
                    E.size(
                        E.qty(E.frac(E.n("4"), E.d("8"))),
                        E.range(E.q1("7"), E.q2("3")),
                        E.unit("cups"),
                        " cold",
                    ),
                ),
                E.item("water"),
            ),
            "1/2 2 - 3 cups warm cups 4/8 7 - 3 cups cold water",
        ),
        # amt.cont
        (
            E.ing(
                E.amt(
                    E.qty(E.frac(E.n("1"), E.d("2"))),
                    E.size(E.range(E.q1("2"), E.q2("3")), E.unit("cups"), " warm"),
                ),
                E.amt(
                    E.unit("cups"),
                    E.size(
                        E.qty(E.frac(E.n("4"), E.d("8"))),
                        E.range(E.q1("7"), E.q2("3")),
                        E.unit("cups"),
                        " cold",
                    ),
                ),
                E.item("water"),
            ),
            "1/2 2 - 3 cups warm cups 4/8 7 - 3 cups cold water",
        ),
        (
            E.ing(
                E.amt(
                    E.qty(E.frac(E.n("1"), E.d("2"))),
                    E.size(E.range(E.q1("2"), E.q2("3")), E.unit("cups"), " warm"),
                ),
                E.sep("or"),
                E.amt(
                    E.unit("cups"),
                    E.size(
                        E.qty(E.frac(E.n("4"), E.d("8"))),
                        E.range(E.q1("7"), E.q2("3")),
                        E.unit("cups"),
                        " cold",
                    ),
                ),
                E.item("water"),
            ),
            "1/2 2 - 3 cups warm or cups 4/8 7 - 3 cups cold water",
        ),
        # modifier
        (
            E.ing(
                E.modifier(
                    "some ",
                    E.size(
                        E.range(E.q1("2"), E.sep(" to "), E.q2("3")),
                        E.unit("cups"),
                        " warm",
                    ),
                    E.amt(E.qty(E.range(E.q1("1"), E.q2("2"))), E.unit("cups")),
                    E.time(E.qty("1"), E.timeunit("hour")),
                    E.frac(E.n("1"), E.d("2")),
                    " cold",
                ),
                E.item("bananas"),
            ),
            "some 2 to 3 cups warm 1 - 2 cups 1 hour 1/2 cold bananas",
        ),
        # prep
        (
            E.ing(
                E.item("bananas"),
                E.prep(
                    "some ",
                    E.size(
                        E.range(E.q1("2"), E.sep(" to "), E.q2("3")),
                        E.unit("cups"),
                        " warm",
                    ),
                    E.amt(E.qty(E.range(E.q1("1"), E.q2("2"))), E.unit("cups")),
                    E.time(E.qty("1"), E.timeunit("hour")),
                    E.frac(E.n("1"), E.d("2")),
                    " cold",
                ),
            ),
            "bananas some 2 to 3 cups warm 1 - 2 cups 1 hour 1/2 cold",
        ),
        # ing-note
        (
            E.ing(
                E.item("bananas"),
                E(
                    "ing-note",
                    "some ",
                    E.size(
                        E.range(E.q1("2"), E.sep(" to "), E.q2("3")),
                        E.unit("cups"),
                        " warm",
                    ),
                    E.amt(E.qty(E.range(E.q1("1"), E.q2("2"))), E.unit("cups")),
                    E.time(E.qty("1"), E.timeunit("hour")),
                    E.frac(E.n("1"), E.d("2")),
                    " cold",
                ),
            ),
            "bananas some 2 to 3 cups warm 1 - 2 cups 1 hour 1/2 cold",
        ),
        # alt-ing
        (
            E.ing(
                E.item("apples"),
                E(
                    "alt-ing",
                    E.item("bananas"),
                    E(
                        "ing-note",
                        "some ",
                        E.size(
                            E.range(E.q1("2"), E.sep(" to "), E.q2("3")),
                            E.unit("cups"),
                            " warm",
                        ),
                        E.amt(E.qty(E.range(E.q1("1"), E.q2("2"))), E.unit("cups")),
                        E.time(E.qty("1"), E.timeunit("hour")),
                        E.frac(E.n("1"), E.d("2")),
                        " cold",
                    ),
                ),
                E("alt-ing", E.item("coconut")),
            ),
            "apples or bananas some 2 to 3 cups warm 1 - 2 cups 1 hour 1/2 cold or coconut",
        ),
        # note
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


@pytest.mark.parametrize(
    "ingredient_elements,ingredient_text",
    [
        (
            (
                E(
                    "ing-div",
                    E.note(
                        "About ",
                        E.amt(E.qty("500"), E.unit("grams")),
                        " of ",
                        E.temp(E.qty("20"), E.tempunit("degree C")),
                        " butter",
                    ),
                    E.ing(E.amt(E.qty("2"), E.unit()), E.item("apples")),
                    E.ing(E.amt(E.qty("3")), E.item("oranges")),
                    E.ing(E.amt(E.qty("5"), E.unit("cups")), E.item("water")),
                    E.note(E.time(E.qty("1"), E.timeunit("hour"))),
                ),
            ),
            (
                "Ingredient Group:",
                "About 500 grams of 20 degree C butter",
                "2 apples",
                "3 oranges",
                "5 cups water",
                "1 hour",
            ),
        ),
        (
            (
                E(
                    "ing-div",
                    E.title("Summer"),
                    E.description("When it's very hot"),
                    E.note(
                        "About ",
                        E.amt(E.qty("500"), E.unit("grams")),
                        " of ",
                        E.temp(E.qty("20"), E.tempunit("degree C")),
                        " butter",
                    ),
                    E.ing(E.amt(E.qty("2"), E.unit()), E.item("apples")),
                    E.ing(E.amt(E.qty("3")), E.item("oranges")),
                    E.ing(E.amt(E.qty("5"), E.unit("cups")), E.item("water")),
                    E.note(E.time(E.qty("1"), E.timeunit("hour"))),
                ),
            ),
            (
                "Ingredient Group: Summer (When it's very hot)",
                "About 500 grams of 20 degree C butter",
                "2 apples",
                "3 oranges",
                "5 cups water",
                "1 hour",
            ),
        ),
        (
            (
                E(
                    "ing-div",
                    E.title("Summer"),
                    E.description("When it's very hot"),
                    E.note(
                        "About ",
                        E.amt(E.qty("500"), E.unit("grams")),
                        " of ",
                        E.temp(E.qty("20"), E.tempunit("degree C")),
                        " butter",
                    ),
                    E.ing(E.amt(E.qty("2"), E.unit()), E.item("apples")),
                    E.ing(E.amt(E.qty("3")), E.item("oranges")),
                    E.ing(E.amt(E.qty("5"), E.unit("cups")), E.item("water")),
                    E.note(E.time(E.qty("1"), E.timeunit("hour"))),
                ),
                E(
                    "ing-div",
                    E.title("Winter"),
                    E.note(
                        "About ",
                        E.amt(E.qty("500"), E.unit("grams")),
                        " of ",
                        E.temp(E.qty("20"), E.tempunit("degree C")),
                        " butter",
                    ),
                    E.ing(E.amt(E.qty("2"), E.unit()), E.item("apples")),
                    E.ing(E.amt(E.qty("3")), E.item("oranges")),
                    E.ing(E.amt(E.qty("5"), E.unit("cups")), E.item("water")),
                    E.note(E.time(E.qty("1"), E.timeunit("hour"))),
                ),
            ),
            (
                "Ingredient Group: Summer (When it's very hot)",
                "About 500 grams of 20 degree C butter",
                "2 apples",
                "3 oranges",
                "5 cups water",
                "1 hour",
                "Ingredient Group: Winter",
                "About 500 grams of 20 degree C butter",
                "2 apples",
                "3 oranges",
                "5 cups water",
                "1 hour",
            ),
        ),
    ],
)
def test_multiple_ingredients_are_correct(
    ingredient_elements: tuple[E, ...], ingredient_text: tuple[str]
) -> None:
    """Assert the ingredients have the right values when there is more than 1."""
    recipe_ml = E.recipeml(E.recipe(E.ingredients(*ingredient_elements)))
    my_cookbook_xml = convert_recipe(recipe_ml)
    ingredients = my_cookbook_xml.xpath("recipe/ingredient/li")
    assert len(ingredients) == len(ingredient_text)
    for i in range(len(ingredient_text)):
        assert ingredients[i].text == ingredient_text[i]
