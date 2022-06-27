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


def test_split_by_sentence(transformer: RecipeTransformer) -> None:
    """Assert that a single step is split into sentences."""
    recipe_ml = E.recipeml(E.recipe(E.directions(E.step(" Step 1.\n\n Step 2 "))))
    my_cookbook_xml = transformer._transform(recipe_ml)
    step_elements = my_cookbook_xml.xpath("recipe/recipetext/li")

    assert len(step_elements) == 2
    assert step_elements[0].text == "Step 1"
    assert step_elements[1].text == "Step 2"
