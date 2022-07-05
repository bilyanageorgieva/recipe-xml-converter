import logging
import tempfile
from pathlib import Path

from lxml.builder import E

from recipe_xml_converter.transformer import (
    CombinedTransformer,
    RecipeTransformer,
    Transformer,
)

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, input_path: str, output_path: str):
        self._input_path = Path(input_path)
        self._output_path = Path(output_path)

    @property
    def _file_paths(self) -> tuple[Path]:
        if self._input_path.is_file():
            return (self._input_path,)
        elif self._input_path.is_dir():
            return tuple(self._input_path.rglob("*.xml"))

    def transform(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            all_files = self._transform_all_recipes(temp_dir)
            file_list_path = self._create_file_list(temp_dir, all_files)
            CombinedTransformer(file_list_path, self._output_path).transform_and_save()

    def _transform_all_recipes(self, temp_dir) -> tuple[Path]:
        all_files = []
        for path in self._file_paths:
            target_path = Path(temp_dir) / path.name
            RecipeTransformer(path, target_path).transform_and_save()
            all_files.append(target_path)

        return tuple(all_files)

    @staticmethod
    def _create_file_list(temp_dir, file_paths) -> Path:
        target_path = Path(temp_dir) / "list_files.xml"
        xml = E.files(*[E.file(path=str(p)) for p in file_paths])
        Transformer.save_to_file(xml, target_path)
        return target_path
