import logging
from pathlib import Path

from lxml import etree as ET

logger = logging.getLogger(__name__)


class Transformer:
    """General transformer class."""

    def __init__(
        self, input_file: str, output_file: str, xsl_files: tuple[Path, ...]
    ) -> None:
        """
        Create a new transformer instance.

        :param input_file: the file to be transformed
        :param output_file: the file location to save the transformed file
        :param xsl_files: the xsl files containing the necessary transformations
        """
        self._input_file = input_file
        self._output_file = output_file
        self._transformations = tuple([ET.XSLT(ET.parse(xsl)) for xsl in xsl_files])

    def transform_and_save(self) -> None:
        """Transform the input file and save the result to the output file."""
        logger.info(f"Parsing {self._input_file}")
        dom = ET.parse(self._input_file)

        logger.info(f"Transforming {self._input_file}")
        dom = self._transform(dom)

        logger.info(f"Saving {self._input_file} to file")
        self._save_to_file(dom)

        logger.info(f"✅ Successfully saved {self._input_file} to {self._output_file}!")

    def _save_to_file(self, dom: ET._XSLTResultTree) -> None:
        """
        Save an XML tree to the desired location in the file system.

        :param dom: the XML tree
        """
        with open(self._output_file, "wb") as file:
            file.write(ET.tostring(dom, pretty_print=True))

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

    def __init__(self, input_file: str, output_file: str):
        """Initialize a new recipe transformer with the correct xsl files."""
        super(RecipeTransformer, self).__init__(
            input_file,
            output_file,
            xsl_files=(
                Path(__file__).parent.parent / "data/stylesheets/transform.xsl",
                Path(__file__).parent.parent / "data/stylesheets/normalize_space.xsl",
            ),
        )
