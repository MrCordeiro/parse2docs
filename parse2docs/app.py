"""Entry point for parse2docs."""
import logging
import os
from argparse import ArgumentParser
from pathlib import Path

from parse2docs.argfinder import get_argparser_from_module
from parse2docs.markdown_renderer import generate_markdown
from parse2docs.module_loader import get_module_from_path

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
        type=Path,
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

    module = get_module_from_path(file_path)
    parser = get_argparser_from_module(module)
    return generate_markdown(parser)


if __name__ == "__main__":
    execute_from_command_line()
