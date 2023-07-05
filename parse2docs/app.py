from argparse import ArgumentParser
import importlib
import inspect
import logging
import os
from typing import Optional
from types import ModuleType

from .markdown_renderer import generate_markdown


logger = logging.getLogger(__name__)


def execute_from_command_line() -> None:
    """Execute parse2docs from the command line."""
    parser = get_argument_parser()
    args = parser.parse_args()
    md = generate_md_from_py_script(args.file_path)
    print(md)


def get_argument_parser() -> ArgumentParser:
    """Get the ArgumentParser for parse2docs."""
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "file_path",
        help="Path to the Python script file containing the ArgumentParser.",
    )
    return arg_parser


def generate_md_from_py_script(file_path: str) -> str:
    """Generate usage documentation in Markdown format.

    Args:
        file_path (str): Path to the Python script file containing the
            ArgumentParser.
    
    Returns:
        str: A string of the usage documentation in Markdown format.
    
    Raises:
        ValueError: If the provided file path does not exist.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"File {file_path} does not exist.")

    module = _get_module_from_path(file_path)
    parser = _find_argparser_in_module(module)
    return generate_markdown(parser)


def _get_module_from_path(path: str) -> ModuleType:
    """Import a Python module from a given path."""
    module_name = _get_module_name(path)
    _navigate_to_path(path)
    return importlib.import_module(module_name)


def _get_module_name(path: str) -> str:
    module_name = path.replace("/", ".").replace("\\", ".")
    if module_name.endswith(".py"):
        module_name = module_name[:-3]
    return module_name


def _navigate_to_path(path: str) -> None:
    script_dir = os.path.dirname(path)
    if script_dir and os.path.basename(os.getcwd()) != script_dir:
        os.chdir(script_dir)


def _find_argparser_in_module(module: ModuleType) -> ArgumentParser:
    """Find ArgumentParser in a given module.

    This function first looks for argparse.ArgumentParser instances in the
    module scope. If it doesn't find any, it then looks for functions that take
    no parameters, executes them, and checks if they return an
    argparse.ArgumentParser instance.

    Returns:
        ArgumentParser: ArgumentParser object from the Python script file.

    Raises:
        ValueError: If no ArgumentParser object is found in the provided file.
    """

    search_functions = [_find_argparser_in_module_scope, _find_argparser_in_functions]
    parser = next((func(module) for func in search_functions if func(module)), None)

    if parser is None:
        raise ValueError("No ArgumentParser object found in the provided file.")

    return parser


def _find_argparser_in_module_scope(module: ModuleType) -> Optional[ArgumentParser]:
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, ArgumentParser):
            return obj


def _find_argparser_in_functions(module: ModuleType) -> Optional[ArgumentParser]:
    for _, obj in inspect.getmembers(module):
        # We only care about functions
        if not inspect.isfunction(obj):
            continue

        try:
            # We only care about functions that take no parameters
            if len(inspect.signature(obj).parameters) > 0:
                continue
            result = obj()
            if isinstance(result, ArgumentParser):
                return result
        # If we can't inspect the function, just skip it
        except TypeError:
            pass


if __name__ == "__main__":
    execute_from_command_line()
