import argparse
import logging
import os
from .wheel_packer import (
    PYTHON_COMPATIBILITY_TAGS_MAPPING,
    PyVerCompatWheelPacker,
    PYTHON_VERSION,
)
from .utils import ensure_directory, ensure_abs

logger = logging.getLogger("")
CWD = os.getcwd()


class LFEnabledFormatter(argparse.HelpFormatter):
    """
    A text formatter for argparse that could show LF
        if the string is started with `R|`
    """

    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)


def ensure_tag_types(args) -> list[list[PYTHON_VERSION]]:
    _tag_types = args.tag_types.split(",")
    tag_types: list[list[PYTHON_VERSION]] = []
    for tag_type in _tag_types:
        tag_type = tag_type.strip()
        if tag_type != "":
            tag_types.append(PYTHON_COMPATIBILITY_TAGS_MAPPING[tag_type])
        assert (
            tag_type in PYTHON_COMPATIBILITY_TAGS_MAPPING
        ), f"Invalid tag type: {tag_type}. All supported tag types are: {list(PYTHON_COMPATIBILITY_TAGS_MAPPING.keys())}"
    return tag_types


def handle_wheel_converter(args):
    tag_types: list[list[PYTHON_VERSION]] = ensure_tag_types(args)
    ensure_directory(wheel_src := ensure_abs(CWD, args.wheel_src))
    ensure_directory(work_dir := ensure_abs(CWD, args.work_dir))
    ensure_directory(wheel_output_dir := ensure_abs(CWD, args.wheel_dir))
    wheel_src = args.wheel_src.split(",")
    PyVerCompatWheelPacker(
        ensure_abs(CWD, "."),
        work_dir,
    ).run(
        tag_types,
        [
            ensure_abs(
                CWD,
                src,
            )
            for src in wheel_src
        ],
        args.ignored_files.split(",") if args.ignored_files else None,
        wheel_output_dir=wheel_output_dir,
    )


parser = argparse.ArgumentParser(
    "Python source code compatibility converter",
)
subparsers = parser.add_subparsers(
    title="Subcommands",
    description="Valid subcommands",
)

wheel_converter_parser = subparsers.add_parser(
    "create-wheel",
    help=(
        "Convert project source code and create wheels "
        "with specific python-compatibility tags"
    ),
    formatter_class=LFEnabledFormatter,
)
wheel_converter_parser.add_argument(
    "--tag-types",
    help=(
        "R|Tag types to build the wheel.\n"
        f"Valid tags are: {list(PYTHON_COMPATIBILITY_TAGS_MAPPING.keys())}. \n"
        f"To build wheels with multiple tags, use ',' to separate different tags."
    ),
    required=True,
)
wheel_converter_parser.add_argument(
    "--wheel-src",
    help=(
        "R|Files or folders needed to build the wheel. \n"
        "If adding a folder, all items under this folder \n"
        "will be copied into the --work-dir recursively"
    ),
    required=True,
)
wheel_converter_parser.add_argument(
    "--ignored-files",
    help=("R|Files or folders to be ignored\n" "If multiple, use ',' to split"),
    required=False,
)
wheel_converter_parser.add_argument(
    "--work-dir",
    help=(
        "Directory to place the temporary files created in the conversion process \n"
        "The Default path is `./pyvercompat` relative to the current working directory"
    ),
    required=False,
    default=os.path.join(os.path.abspath(os.getcwd()), ".pyvercompat-workdir"),
)
wheel_converter_parser.add_argument(
    "--wheel-dir",
    help="Folder to place the generated wheels, `dist` by default",
    required=False,
    default=os.path.join(os.path.abspath(os.getcwd()), "pyvercompat-dist"),
)
wheel_converter_parser.set_defaults(func=handle_wheel_converter)
args = parser.parse_args()
args.func(args)
