"""
This file is used to pack up wheels, and convert the wheel to specific version
"""

import os


class PyVerCompatWheelPacker:
    def __init__(self, work_dir: str, resources_to_copy: list[str]) -> None:
        self.work_dir = work_dir
        self.wheel_dir = os.path.join(self.work_dir, "wheel")
        self.resources_to_copy = resources_to_copy
        # for src in self.resources_to_copy:
        #     if os.path.isfile(src):
        #         pass

    def get_abspath(self, relpath: str):
        return os.path.join(self.work_dir, relpath)
