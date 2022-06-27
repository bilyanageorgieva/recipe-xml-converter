import pytest as pytest

from recipe_xml_converter.transformer import RecipeTransformer


@pytest.fixture
def transformer() -> RecipeTransformer:
    return RecipeTransformer("", "")
