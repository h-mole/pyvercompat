import os
import sys

from pyvercompat import (
    PyVerCompatWheelPacker,
    convert_file,
    PY_OVER_310,
    PY_SUB_310,
    PY_38_39,
)
from pyvercompat.utils import ensure_abs

current_file_folder = os.path.abspath(os.path.dirname(__file__))
assets_folder = os.path.join(current_file_folder, "assets")
outputs_folder = os.path.join(current_file_folder, "output")


def test_packup():
    packer = PyVerCompatWheelPacker(
        os.path.join(assets_folder, "demo_package"), outputs_folder
    )
    packer.run(
        [PY_OVER_310, PY_38_39],
        [ensure_abs(packer.sourcefile_dir, item) for item in ["UppaalLTLParser", "README.md", "setup.py"]],
        wheel_output_dir=os.path.join(outputs_folder, "dist"),
        ignored_file_types=[".pyc"],
    )
