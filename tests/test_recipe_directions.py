import pytest
from lxml.builder import E

from recipe_xml_converter.transformer import RecipeTransformer
from tests.fixtures import transformer  # noqa: F401


def test_correct_number_of_steps(transformer: RecipeTransformer) -> None:
    """Assert the correct number of steps have been created."""
    step_num = 5
    recipe_ml = E.recipeml(E.recipe(E.directions(*[E.step() for _ in range(step_num)])))
    my_cookbook_xml = transformer._transform(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/recipetext/li")) == step_num


def test_steps_are_correct(transformer: RecipeTransformer) -> None:
    """Assert the steps have the right values."""
    steps = ["Step 1", "Step 2"]
    recipe_ml = E.recipeml(E.recipe(E.directions(*[E.step(step) for step in steps])))
    my_cookbook_xml = transformer._transform(recipe_ml)
    step_elements = my_cookbook_xml.xpath("recipe/recipetext/li")

    for i, cat in enumerate(steps):
        assert cat == step_elements[i].text


@pytest.mark.parametrize(
    "directions,transformed",
    [
        (
            E.directions(
                E.note(
                    "About ",
                    E.amt(E.qty("500"), E.unit("grams")),
                    " of ",
                    E.temp(E.qty("20"), E.tempunit("degree C")),
                    " butter",
                ),
                E.step(
                    E.action("Blend the butter with the sugar "),
                    E.condition("only if melted"),
                ),
            ),
            (
                "About 500 grams of 20 degree C butter",
                "Blend the butter with the sugar only if melted",
            ),
        ),
        (
            E.directions(
                E.note(
                    "About ",
                    E.amt(E.qty("500"), E.unit("grams")),
                    " of ",
                    E.temp(E.qty("20"), E.tempunit("degree C")),
                    " butter",
                ),
                E.step(
                    E.substep(E.action("Make sure the butter is soft.")),
                    E.substep(E.condition("Stir it with the sugar.")),
                    " Put some sprinkles.",
                ),
            ),
            (
                "About 500 grams of 20 degree C butter",
                "Make sure the butter is soft. Stir it with the sugar. Put some sprinkles.",
            ),
        ),
        (
            E.directions(
                E(
                    "dir-div",
                    E.title("Preparing the dough"),
                    E.description("24 hours in advance"),
                    E.step(
                        E.action("Make the dough and leave it."),
                    ),
                    E.step(
                        E.action("Cover with a towel"),
                        E.condition("if cold"),
                    ),
                ),
                E(
                    "dir-div",
                    E.title("Something else"),
                    E.step(E.action("Do another thing.")),
                ),
                E(
                    "dir-div",
                    E.description("One final thing."),
                    E.step(
                        "Use the ",
                        E.tool(E.brandname("SomeBrand"), " airfryer"),
                        " to cook the potatoes",
                    ),
                ),
                E(
                    "dir-div",
                    E.step("This is only a step"),
                ),
            ),
            (
                "Directions Group: Preparing the dough (24 hours in advance)",
                "Make the dough and leave it.",
                "Cover with a towel if cold",
                "Directions Group: Something else",
                "Do another thing.",
                "Directions Group: One final thing.",
                "Use the SomeBrand airfryer to cook the potatoes",
                "Directions Group:",
                "This is only a step",
            ),
        ),
    ],
)
def test_directions(
    transformer: RecipeTransformer, directions: E, transformed: tuple[str, ...]
) -> None:
    """Assert the directions are transformed correctly."""
    recipe_ml = E.recipeml(E.recipe(directions))
    my_cookbook_xml = transformer._transform(recipe_ml)
    step_elements = my_cookbook_xml.xpath("recipe/recipetext/li")

    print([e.text for e in step_elements])
    assert len(step_elements) == len(transformed)
    for i in range(len(step_elements)):
        assert step_elements[i].text == transformed[i]
