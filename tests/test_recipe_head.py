from lxml.builder import E

from recipe_xml_converter.converter import convert_recipe


def test_title_exists() -> None:
    """Assert the title element exists."""
    recipe_ml = E.recipeml(E.recipe(E.head(E.title("Recipe Title"))))
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
    assert len(my_cookbook_xml.xpath("recipe/title")) == 1
    assert my_cookbook_xml.xpath("recipe/title")[0].text == title


def test_no_categories() -> None:
    """Assert no category tags are created when there are no categories."""
    recipe_ml = E.recipeml(E.recipe(E.head()))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert not my_cookbook_xml.xpath("recipe/category")


def test_categories_created() -> None:
    """Assert the right number of categories are created."""
    categories = 2
    recipe_ml = E.recipeml(
        E.recipe(E.head(E.categories(*[E.cat() for _ in range(categories)])))
    )
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/category")) == categories


def test_categories_are_correct() -> None:
    """Assert the categories have the right values."""
    categories = ["Category 1", "Category 2"]
    recipe_ml = E.recipeml(
        E.recipe(E.head(E.categories(*[E.cat(cat) for cat in categories])))
    )
    my_cookbook_xml = convert_recipe(recipe_ml)
    category_elements = my_cookbook_xml.xpath("recipe/category")

    for i, cat in enumerate(categories):
        assert cat == category_elements[i].text


def test_no_yield() -> None:
    """Assert no quantity tags are created when there is no yield."""
    recipe_ml = E.recipeml(E.recipe(E.head()))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert not my_cookbook_xml.xpath("recipe/quantity")


def test_yield_is_correct() -> None:
    """Assert the quantity is correct."""
    yield_ = "12"
    recipe_ml = E.recipeml(E.recipe(E.head(E("yield", yield_))))
    my_cookbook_xml = convert_recipe(recipe_ml)
    quantity = my_cookbook_xml.xpath("recipe/quantity")
    assert quantity[0].text == yield_
