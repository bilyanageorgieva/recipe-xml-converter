import abc
import logging
import tempfile
import time
import uuid
import zipfile
from pathlib import Path
from typing import IO, Optional, Type, Union

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
        self,
        input_files: tuple[Union[Path, IO], ...],
        output_dir: Path,
        max_files_combined: int = 1000,
    ) -> None:
        """
        Initialize a new orchestrator instance.

        :param input_files: the full paths to the input files to transform
        :param output_dir: the full path to the target folder where the transformation results should be saved
        :param max_files_combined: the maximum number of files to combine into one
        """
        self._input_files = input_files
        self._output_dir = output_dir
        self._max_files_combined = max_files_combined

    @property
    @abc.abstractmethod
    def _transformer_class(self) -> Type[Transformer]:
        """Return the transformer to use to transform the individual files."""

    @property
    @abc.abstractmethod
    def _combiner_class(self) -> Type[Transformer]:
        """Return the transformer to use to combine the transformed files."""

    def orchestrate(self) -> Path:
        """
        Transform and combine all input files saving the result to the target location as a zip archive.

        :return: the path to the zip archive
        """
        with tempfile.TemporaryDirectory() as work_dir:
            transformed_files = self._transform_files(Path(work_dir))
            logger.info(
                f"Successfully transformed {len(transformed_files)}/{len(self._input_files)} files."
            )

            file_lists = self._generate_file_lists(transformed_files, Path(work_dir))
            logger.info(f"Generated {len(file_lists)} file lists.")

            combined_files = self._combine_files(file_lists, Path(work_dir))
            logger.info(
                f"Combined all {len(transformed_files)} transformed files into {len(combined_files)} files."
            )

            return self.zip_files(combined_files)

    def zip_files(self, file_paths: tuple[Path, ...]) -> Path:
        """
        Create a zip archive containing the XML files defined changing their names with consecutive numbers.

        :param file_paths: the full paths to the files to include in the archive
        :return: the full path to the archive
        """
        archive_path = self._output_dir / f"{int(time.time())}_transformed.zip"
        with zipfile.ZipFile(archive_path, mode="w") as archive:
            for i, file in enumerate(file_paths):
                archive.write(file, f"{i+1}.xml")
        return archive_path

    def _transform_files(self, target_dir: Path) -> tuple[Path, ...]:
        """
        Transform all files and save them to the target directory.

        :param target_dir: the full path to the directory where to save the files
        :return: the full paths to all the created files
        """
        all_files = [
            self._transform_file(file, target_dir)
            for file in tqdm(self._input_files, desc="Files processed")
        ]
        return tuple([file for file in all_files if file])

    def _combine_files(
        self, file_lists: tuple[Path, ...], target_dir: Path
    ) -> tuple[Path, ...]:
        """
        Combine the files in the file list and save the result in the target directory.

        :param file_lists: the full path to the XML listing all files to be combined
        """
        combined_files = []
        for file_list in file_lists:
            target_path = target_dir / f"{uuid.uuid4()}.xml"
            self._combiner_class(file_list, target_path).transform_and_save()
            combined_files.append(target_path)
        return tuple(combined_files)

    def _transform_file(
        self, file: Union[Path, IO], target_dir: Path
    ) -> Optional[Path]:
        """
        Transform one file and save it to the target directory.

        :param file: the full path to the file to be transformed
        :param target_dir: the full path to the target directory to save the transformed file
        :return: the full path to the transformed file
        """
        target_path = Path(target_dir) / f"{uuid.uuid4()}.xml"
        try:
            self._transformer_class(file, target_path).transform_and_save()
            return target_path
        except TransformerException:
            logger.exception(f"❌ Failed to transform {file.name}")
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
