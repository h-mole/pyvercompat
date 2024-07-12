"""
This file is used to pack up wheels, and convert the wheel to specific version
"""

import glob
import logging
import os
import shutil
import sys
import tempfile
from typing import Literal, Optional
from .converter import convert_file
from .utils import last_item_of_fs_item

# Python version tags are specified in
# https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#python-tag
PYTHON_VERSION = Literal[
    "py36", "py37", "py38", "py39", "py310", "py311", "py312", "py313"
]
PY_SUB_38: list[PYTHON_VERSION] = ["py36", "py37"]
PY_SUB_310: list[PYTHON_VERSION] = ["py36", "py37", "py38", "py39"]
PY_39: list[PYTHON_VERSION] = ["py39"]
PY_38_39: list[PYTHON_VERSION] = ["py38", "py39"]
PY_OVER_310: list[PYTHON_VERSION] = ["py310", "py311", "py312", "py313"]

PYTHON_COMPATIBILITY_TAGS_MAPPING: dict[str, list[PYTHON_VERSION]] = {
    "38-39": PY_38_39,
    "39": PY_39,
    "310+": PY_OVER_310,
}


class PyVerCompatWheelPacker:
    def __init__(self, sourcefile_dir: str, work_dir: str) -> None:
        """
        :sourcefile_dir: A directory containing source code to be packed up. There should be a `setup.py` or `pyproject.toml` inside it.
        :work_dir: A directory to temporarily store the converted files
        """
        self.sourcefile_dir = sourcefile_dir
        self.work_dir = work_dir
        self._logger = logging.getLogger("pyvercompat." + self.__class__.__name__)

    def get_wd_item_abspath(self, relpath: str):
        return os.path.join(self.work_dir, relpath)

    def copy_resources(
        self,
        current_dir: str,
        target_dir: str,
        resources_to_copy: list[str],
        ignored_file_types: set[str],
    ):
        """
        Copy resources to the target directory
        """
        for resource in resources_to_copy:

            assert os.path.isabs(resource)
            source_path = resource
            destination_path = os.path.join(target_dir, last_item_of_fs_item(resource))
            if os.path.isfile(source_path) and (
                os.path.splitext(source_path)[1] not in ignored_file_types
            ):
                shutil.copy2(source_path, destination_path)
            else:
                shutil.copytree(source_path, destination_path)

    def convert_tree(
        self,
        directory: str,
        target_dir: str,
        ignored_file_types: set[str],
    ):
        """
        Traverse the directory and copy all files to the target directory, except those with the specified file extensions.

        :directory: The directory to traverse
        :target_dir: Converted files will be written to the `target_dir`
        :ignored_file_types: A list of file extensions to ignore (should be passed with a dot, e.g. ".txt")
        """
        for ignored_ext in ignored_file_types:
            assert ignored_ext.startswith(
                "."
            ), f"ignored file types should be passed with prefix '.', but passed '{ignored_ext}'"

        os.makedirs(target_dir, exist_ok=True)

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1]
                target_file_path = os.path.join(
                    target_dir, os.path.relpath(file_path, directory)
                )
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                if file_extension == ".py":
                    convert_file(file_path, target_file_path)
                elif file_extension not in ignored_file_types:
                    shutil.copy2(file_path, target_file_path)
                    # print(f"Copied {file_path} to {target_file_path}")

    def pack_up(
        self,
        target_dir: str,
        supported_python_versions: list[PYTHON_VERSION],
        wheel_output_dir: str,
    ):
        """
        Pack up the wheel and assign python version tags in its filename.

        :target_dir: The directory containing the package. There should be a `setup.py` or `pyproject.toml` inside it.
        :supported_python_versions: A list of python version tags. If empty, the wheel will be created for all python3 versions
        :wheel_output_dir: The directory to store the built wheels.
        """
        assert os.path.isabs(wheel_output_dir)
        original_dir = os.getcwd()
        os.chdir(target_dir)
        supported_python_versions.sort()
        py_versions_tag = (
            ".".join(supported_python_versions)
            if len(supported_python_versions) > 0
            else "py3"
        )
        # Create a temporary folder to store the built wheel, then change its python tag to the supported versions
        with tempfile.TemporaryDirectory() as temp_dir:
            os.system(f"{sys.executable} -m pip wheel . --wheel-dir {temp_dir}")
            whl_files = glob.glob(os.path.join(temp_dir, "*.whl"))
            whl_file = whl_files[0]
            os.system(
                f"{sys.executable} -m wheel tags --python-tag={py_versions_tag} --abi-tag=none --remove {whl_file}"
            )
            wheel_filename = os.path.basename(
                glob.glob(os.path.join(temp_dir, "*.whl"))[0]
            )
            logging.info(
                f"Copying created wheel {wheel_filename} to {wheel_output_dir}"
            )
            shutil.copyfile(
                os.path.join(temp_dir, wheel_filename),
                os.path.join(wheel_output_dir, wheel_filename),
            )
        os.chdir(original_dir)

    @classmethod
    def _remove_contents(cls, dir_path: str):
        """
        Remove all contents of a directory
        """
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def run(
        self,
        pytags4whl: list[list[PYTHON_VERSION]],
        resources_to_copy: list[str],
        ignored_file_types: Optional[list[str]] = None,
        wheel_output_dir: str = "dist",
        interactive=True,
    ):
        """
        Major procedure of packing tool.

        :pytags4whl: A list containing the python version tags for each created low-version wheels.
            for example, `[PY_38_39, PY_OVER_310]` will create two wheels:
            1. `NAME-VERSION-py38.py39-none-any.whl`
            2. `NAME-VERSION-py310.py311.py312.py313-none-any.whl`

            NOTICE: Items in this list must match tags specified in the body of this method

        :resources_to_copy: A list of relative paths specifying resources to be copied for building wheels.
        :ignored_file_types: A list of file extensions to ignore (should be passed with a dot, e.g. ".pyc")
        :wheel_output_dir: The directory to store the generated .whl files, must be absolute.
        """
        assert os.path.isabs(
            wheel_output_dir
        ), f"Parameter wheel_output_dir {wheel_output_dir} should be an absolute path!"
        _ignored_file_types_set: set[str] = set((ignored_file_types or []) + [".pyc"])
        print("wheel src", resources_to_copy)
        if os.path.exists(self.work_dir):
            if interactive:
                ret = input(
                    f"Work directory {self.work_dir} not empty, remove it? (y/N) "
                )
                if ret != "y":
                    print("Cancelled")
                    return
            self._remove_contents(self.work_dir)

        dir_original_sourcecode = self.get_wd_item_abspath("original-sourcecode")
        self._logger.info(
            f"Copying source code from {self.sourcefile_dir} to work directory {dir_original_sourcecode}"
        )
        self.copy_resources(
            self.sourcefile_dir,
            dir_original_sourcecode,
            resources_to_copy,
            _ignored_file_types_set,
        )
        self._logger.info(
            f"Copied source code to work directory {dir_original_sourcecode}"
        )
        for wheel_tags in pytags4whl:
            wheel_tags_str = ".".join(wheel_tags)
            dir_converted_sourcecode = self.get_wd_item_abspath(
                f"converted-sourcecode-{wheel_tags_str}"
            )

            self.convert_tree(
                dir_original_sourcecode,
                dir_converted_sourcecode,
                _ignored_file_types_set,
            )
            self._logger.info(
                f"Converted original source code to version {wheel_tags_str} at directory {dir_converted_sourcecode}"
            )
            self.pack_up(
                dir_converted_sourcecode,
                wheel_tags,
                wheel_output_dir=wheel_output_dir,
            )
            self._logger.info(
                f"Packed up the wheel tagged {wheel_tags_str} at directory {dir_converted_sourcecode}"
            )
        self._logger.info(f"Packed up all wheels, placing at {wheel_output_dir}")
