import logging
import sys
from .converter import convert_file
from .wheel_packer import (
    PyVerCompatWheelPacker,
    PY_SUB_310,
    PY_SUB_38,
    PYTHON_VERSION,
    PY_OVER_310,
    PY_38_39,
)

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
