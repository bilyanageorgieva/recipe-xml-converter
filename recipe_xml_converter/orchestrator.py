import abc
import logging
import tempfile
import time
import uuid
from pathlib import Path
from typing import Optional, Type

from lxml.builder import E
from tqdm import tqdm

from recipe_xml_converter.exceptions import TransformerException
from recipe_xml_converter.transformer import (
    RecipeCombiner,
    RecipeTransformer,
    Transformer,
)

logger = logging.getLogger(__name__)


class Orchestrator(abc.ABC):
    """General orchestrator for a complete workflow of transforming and combining multiple XML files."""

    def __init__(
        self, input_path: str, output_path: str, max_files_combined: int
    ) -> None:
        """
        Initialize a new orchestrator instance.

        :param input_path: the full path to the input file or folder
        :param output_path: the full path to the target folder where the transformation results should be saved
        :param max_files_combined: the maximum number of files to combine into one
        """
        self._input_path = Path(input_path)
        self._output_path = Path(output_path) / f"{int(time.time())}_transformed"
        self._max_files_combined = max_files_combined

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

    def orchestrate(self) -> None:
        """Orchestrate the transformation and combining of all input files saving the result to the target location."""
        with tempfile.TemporaryDirectory() as work_dir:
            transformed_files = self._transform_files(Path(work_dir))
            logger.info(
                f"Successfully transformed {len(transformed_files)}/{len(self._file_paths)} files."
            )

            file_lists = self._generate_file_lists(transformed_files, Path(work_dir))
            logger.info(f"Generated {len(file_lists)} file lists.")

            self._combine_files(file_lists)
            logger.info(
                f"✅ Stored all {len(file_lists)} transformed files in {self._output_path}"
            )

    def _transform_files(self, target_dir: Path) -> tuple[Path, ...]:
        """
        Transform all files and save them to the target directory.

        :param target_dir: the full path to the directory where to save the files
        :return: the full paths to all the created files
        """
        all_files = [
            self._transform_file(file, target_dir)
            for file in tqdm(self._file_paths, desc="Files processed")
        ]
        return tuple([file for file in all_files if file])

    def _combine_files(self, file_lists: tuple[Path, ...]) -> None:
        """
        Combine the files in the file list and save the result in the target location.

        :param file_lists: the full path to the XML listing all files to be combined
        """
        for i, file_list in enumerate(file_lists):
            self._combiner_class(
                file_list, self._output_path / f"{i + 1}.xml"
            ).transform_and_save()

    def _transform_file(self, file: Path, target_dir: Path) -> Optional[Path]:
        """
        Transform one file and save it to the target directory.

        :param file: the full path to the file to be transformed
        :param target_dir: the full path to the target directory to save the transformed file
        :return: the full path to the transformed file
        """
        target_path = Path(target_dir) / f"{uuid.uuid4()}.xml"
        try:
            with open(file) as f:
                self._transformer_class(f, target_path).transform_and_save()
            return target_path
        except TransformerException:
            logger.exception(f"❌ Failed to transform {file}")
            return None

    def _generate_file_lists(
        self, files: tuple[Path, ...], target_dir: Path
    ) -> tuple[Path, ...]:
        """
        Generate and save XMLs listing all files to be combined respecting the maximum files allowed.

        :param files: the full paths to the files to be included in the list
        :param target_dir: the target directory to save the file list
        :return: the full path to the file list
        """
        file_groups = [
            files[i : i + self._max_files_combined]
            for i in range(0, len(files), self._max_files_combined)
        ]
        file_lists = [
            self._generate_file_list(group, target_dir)
            for group in tqdm(file_groups, "Generated file groups")
        ]
        return tuple(file_lists)

    @staticmethod
    def _generate_file_list(files: tuple[Path, ...], target_dir: Path) -> Path:
        """
        Generate an XML listing all the files to be combined and save it to the target directory.

        :param files: the full paths to the files to be included in the list
        :param target_dir: the target directory to save the file list
        :return: the full path to the file list
        """
        target_path = Path(target_dir) / f"{uuid.uuid4()}.xml"
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
