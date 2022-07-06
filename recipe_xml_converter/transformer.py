import abc
import logging
from pathlib import Path
from typing import Union

from lxml import etree as ET

from recipe_xml_converter.exceptions import TransformerException

logger = logging.getLogger(__name__)


class Transformer(abc.ABC):
    """General transformer class."""

    def __init__(self, input_file: Path, output_file: Path) -> None:
        """
        Create a new transformer instance.

        :param input_file: the file to be transformed
        :param output_file: the file location to save the transformed file
        """
        self._input_file = input_file
        self._output_file = output_file

    @property
    @abc.abstractmethod
    def _xsl_files(self) -> tuple[Path, ...]:
        """Return the XSL files containing the transformations in the right order."""

    @property
    def _transformations(self) -> tuple[ET.XSLT, ...]:
        """Return the parsed XSL transformations in the right order."""
        return tuple([ET.XSLT(ET.parse(xsl)) for xsl in self._xsl_files])

    def transform_and_save(self) -> None:
        """Transform the input file and save the result to the output file."""
        logger.debug(f"Parsing {self._input_file}")
        dom = self._parse_input()

        logger.debug(f"Transforming {self._input_file}")
        dom = self._transform(dom)

        logger.debug(f"Saving {self._input_file} to file")
        self.save_to_file(dom, self._output_file)

        logger.info(f"✅ Successfully saved {self._input_file} to {self._output_file}")

    def _parse_input(self) -> ET._ElementTree:
        """Parse the input file and return the ElementTree."""
        try:
            return ET.parse(self._input_file)
        except ET.XMLSyntaxError as e:
            raise TransformerException(f"Failed to parse {self._input_file}", e)

    @staticmethod
    def save_to_file(dom: ET._ElementTree, file_path: Union[str, Path]) -> None:
        """
        Save an XML dom to a file.

        :param dom: the XML dom representation to save
        :param file_path: the target path to save the XML
        """
        with open(file_path, "wb") as file:
            file.write(
                ET.tostring(
                    dom, pretty_print=True, xml_declaration=True, encoding="UTF-8"
                )
            )

    def _transform(self, dom: ET._ElementTree) -> ET._XSLTResultTree:
        """
        Transform an XML tree using the defined XSL transformations.

        :param dom: the XML tree to be transformed
        :return: the transformed tree
        """
        for transformation in self._transformations:
            dom = transformation(dom)
        return dom


class RecipeTransformer(Transformer):
    """A transformer from RecipeML to My Cookbook XML."""

    @property
    def _xsl_files(self) -> tuple[Path, ...]:
        """Return the XSL files defining the recipe transformations."""
        return (
            Path(__file__).parent.parent / "stylesheets/transform.xsl",
            Path(__file__).parent.parent / "stylesheets/normalize_space.xsl",
        )


class RecipeCombiner(Transformer):
    """Combines multiple MyCookbook XML files specified in a file."""

    @property
    def _xsl_files(self) -> tuple[Path, ...]:
        """Return the XSL files defining the transformations for combining the recipes."""
        return (Path(__file__).parent.parent / "stylesheets/group.xsl",)
