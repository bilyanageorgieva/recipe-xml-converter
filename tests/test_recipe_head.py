from lxml.builder import E
import pytest

from recipe_xml_converter.converter import convert_recipe


@pytest.mark.parametrize(
    "recipe_ml_el,my_cookbook_el",
    [
        ("title", "title"),
        ("subtitle", "description"),
    ],
)
def test_title_exists(recipe_ml_el: str, my_cookbook_el: str) -> None:
    """Assert the element exists."""
    recipe_ml = E.recipeml(E.recipe(E.head(E(recipe_ml_el, ""))))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert my_cookbook_xml.xpath(f"recipe/{my_cookbook_el}")


def test_title_exists_without_value() -> None:
    """Assert the title element exists even when the original title is missing."""
    recipe_ml = E.recipeml(E.recipe(E.head(E.title())))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert my_cookbook_xml.xpath("recipe/title")


@pytest.mark.parametrize(
    "element,text",
    [
        (E.title("Original Title"), "Original Title"),
        (E.title("Original ", E.span("Title")), "Original Title"),
        (
            E.title(
                "Original ",
                E.brandname("Lays ", E.span("Chips")),
                " for ",
                E.span(E.frac(E.n("3"), E.sep(" to "), E.d("4")), " people"),
            ),
            "Original Lays Chips for 3 to 4 people",
        ),
        (
            E.title(
                "Original ",
                E.brandname("Lays ", E.span("Chips")),
                " for ",
                E.span(E.frac(E.n("3"), E.d("4")), " people"),
            ),
            "Original Lays Chips for 3/4 people",
        ),
    ],
)
def test_title_is_correct(element: E, text: str) -> None:
    """Assert the title has correct value."""
    recipe_ml = E.recipeml(E.recipe(E.head(element)))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/title")) == 1
    assert my_cookbook_xml.xpath("recipe/title")[0].text == text


@pytest.mark.parametrize(
    "element,text",
    [
        (E.subtitle("Original Title"), "Original Title"),
        (E.subtitle("Original ", E.span("Title")), "Original Title"),
        (
            E.subtitle(
                "Original ",
                E.brandname("Lays ", E.span("Chips")),
                " for ",
                E.span(E.frac(E.n("3"), E.sep(" to "), E.d("4")), " people"),
            ),
            "Original Lays Chips for 3 to 4 people",
        ),
        (
            E.subtitle(
                "Original ",
                E.brandname("Lays ", E.span("Chips")),
                " for ",
                E.span(E.frac(E.n("3"), E.d("4")), " people"),
            ),
            "Original Lays Chips for 3/4 people",
        ),
    ],
)
def test_title_is_correct(element: E, text: str) -> None:
    """Assert the title has correct value."""
    recipe_ml = E.recipeml(E.recipe(E.head(element)))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert len(my_cookbook_xml.xpath("recipe/description")) == 1
    assert my_cookbook_xml.xpath("recipe/description")[0].text == text


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


def test_recipe_source_exists() -> None:
    """Assert the recipe source element exists."""
    recipe_ml = E.recipeml(E.recipe(E.head(E.source())))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert len(my_cookbook_xml.xpath("source/li")) == 1


@pytest.mark.parametrize(
    "element,text",
    [
        (E.source("Some source"), "Some source"),
        (E.source("Original ", E.srcitem("Source")), "Original Source"),
        (
            E.source(
                "Original ",
                E.srcitem("Lays ", E.span("Chips"), type="DC.Creator"),
                " created on ",
                E.srcitem("12.03.2020", type="DC.Date"),
            ),
            "Original Lays Chips created on 12.03.2020",
        ),
    ],
)
def test_recipe_source_is_correct(element: E, text: str) -> None:
    """Assert the recipe source element has the correct value."""
    recipe_ml = E.recipeml(E.recipe(E.head(element)))
    my_cookbook_xml = convert_recipe(recipe_ml)
    assert len(my_cookbook_xml.xpath("source/li")) == 1
    assert my_cookbook_xml.xpath("source/li")[0].text == text
