from pathlib import Path

import pytest as pytest

from recipe_xml_converter.transformer import RecipeTransformer


@pytest.fixture
def transformer() -> RecipeTransformer:
    """Create a basic transformer to use for all tests that don't save to the file system."""
    return RecipeTransformer(Path(), Path())
