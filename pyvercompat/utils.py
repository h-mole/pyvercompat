import ast
import inspect
import os
from pyvercompat.converter import TransformerToLegacy
import logging

logging.basicConfig(level=logging.INFO)


def last_item_of_fs_item(path: str):
    if os.path.isfile(path):
        return os.path.basename(path)
    else:
        return os.path.basename(os.path.normpath(path))


def ensure_directory(dir: str):
    """
    Ensure directory exists
    """
    os.makedirs(dir, exist_ok=True)


def ensure_abs(dir_if_rel: str, path: str):
    """
    Ensure path is absolute
    """
    if os.path.isabs(path):
        return path
    else:
        return os.path.join(dir_if_rel, path)


def ensure_same_functionality(
    func: "function", args_list: list[tuple], show_converted_code=False
):
    """
    Ensure same functionality for the same function and arguments

    Specialized for testing
    """
    logger = logging.getLogger(ensure_same_functionality.__name__)
    logger.setLevel(logging.INFO)
    func_not_converted = func
    func_src = inspect.getsource(func_not_converted)
    converted_code = ast.unparse(TransformerToLegacy().visit(ast.parse(func_src)))
    if show_converted_code:
        print(f"Converted code of {func.__name__}: \n{converted_code}")
    globals_for_exec = {}
    exec(converted_code, globals_for_exec)
    func_converted = globals_for_exec[func_not_converted.__name__]
    for arg_value in args_list:
        res_not_converted = func_not_converted(*arg_value)
        res_converted = func_converted(*arg_value)
        if res_not_converted != res_converted:
            raise ValueError(
                f"""
INPUT: {arg_value}
ORIG_FCN_OUT: {res_not_converted} 
CONV_FCN_OUT: {res_converted}
"""
            )
