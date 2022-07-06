import abc
import logging
import tempfile
from pathlib import Path
from typing import Type

from lxml.builder import E

from recipe_xml_converter.transformer import (
    RecipeCombiner,
    RecipeTransformer,
    Transformer,
)

logger = logging.getLogger(__name__)


class Orchestrator(abc.ABC):
    """General orchestrator for a complete workflow of transforming and combining multiple files."""

    def __init__(self, input_path: str, output_path: str) -> None:
        """
        Initialize a new orchestrator instance.

        :param input_path: the full path to the input file or folder
        :param output_path: the full path to the target file where the transformation results should be saved
        """
        self._input_path = Path(input_path)
        self._output_path = Path(output_path)

    @property
    @abc.abstractmethod
    def _transformer_class(self) -> Type[Transformer]:
        """Return the transformer to use to transform the individual files."""

    @property
    @abc.abstractmethod
    def _combiner_class(self) -> Type[Transformer]:
        """Return the transformer to use to combine the transformed files."""

    @property
    def _file_paths(self) -> tuple[Path, ...]:
        """Return the paths to all files to be processed."""
        if self._input_path.is_file():
            return (self._input_path,)
        elif self._input_path.is_dir():
            return tuple(self._input_path.rglob("*.xml"))
        else:
            raise ValueError(f"Cannot locate input file(s) at {self._input_path}")

    def transform(self) -> None:
        """Transform all input files and combine them to a single one saving it to the target location."""
        with tempfile.TemporaryDirectory() as temp_dir:
            all_files = self._transform_files(Path(temp_dir))
            file_list = self._generate_file_list(all_files, Path(temp_dir))
            self._combine_files(file_list)

    def _transform_files(self, target_dir: Path) -> tuple[Path, ...]:
        """
        Transform all files and save them to the target directory.

        :param target_dir: the full path to the directory where to save the files
        :return: the full paths to all the created files
        """
        return tuple(
            [self._transform_file(file, target_dir) for file in self._file_paths]
        )

    def _combine_files(self, file_list: Path) -> None:
        """
        Combine the files in the file list and save the result in the target location.

        :param file_list: the full path to the XML listing all files to be combined
        """
        self._combiner_class(file_list, self._output_path).transform_and_save()

    def _transform_file(self, file: Path, target_dir: Path) -> Path:
        """
        Transform one file and save it to the target directory.

        :param file: the full path to the file to be transformed
        :param target_dir: the full path to the target directory to save the transformed file
        :return: the full path to the transformed file
        """
        target_path = Path(target_dir) / file.name
        self._transformer_class(file, target_path).transform_and_save()
        return target_path

    @staticmethod
    def _generate_file_list(files: tuple[Path, ...], target_dir: Path) -> Path:
        """
        Generate an XML listing all the files to be combined and save it to the target directory.

        :param files: the full paths to the files to be included in the list
        :param target_dir: the target directory to save the file list
        :return: the full path to the file list
        """
        target_path = Path(target_dir) / "list_files.xml"
        dom = E.files(*[E.file(path=str(path)) for path in files])
        Transformer.save_to_file(dom, target_path)
        return target_path


class RecipeOrchestrator(Orchestrator):
    """Orchestrator to transform RecipeML files into a single MyCookbook XML file."""

    @property
    def _transformer_class(self) -> Type[Transformer]:
        """Return the recipe transformer class."""
        return RecipeTransformer

    @property
    def _combiner_class(self) -> Type[Transformer]:
        """Return the recipe combiner class."""
        return RecipeCombiner
