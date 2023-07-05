from argparse import ArgumentParser

import pytest

from parse2docs.markdown_renderer import (
    _add_description,
    _add_overall_usage,
    _add_table_of_contents,
    _document_action,
    generate_markdown,
)


@pytest.fixture
def parser():
    parser = ArgumentParser(description="A simple file copy script.")
    parser.add_argument(
        "-s",
        "--source",
        metavar="source_path",
        type=str,
        required=True,
        help="Source file path",
    )
    parser.add_argument(
        "-d",
        "--destination",
        metavar="dest_path",
        type=str,
        required=True,
        help="Destination file path",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    return parser


@pytest.fixture
def empty_parser():
    return ArgumentParser(description="A script with no options.")


def test_generate_markdown(parser: ArgumentParser):
    markdown = generate_markdown(parser)
    assert "# Usage Documentation" in markdown
    assert "## Description" in markdown
    assert "A simple file copy script." in markdown
    assert "## Overall Usage Example" in markdown
    assert "## Table of Contents" in markdown
    assert "## Options" in markdown


def test_generate_markdown_on_empty_parser(empty_parser: ArgumentParser):
    markdown = generate_markdown(empty_parser)
    assert (
        "## Options" not in markdown
    ), "Options section should not be present on a parser with no arguments"


def test_add_description(parser):
    description = _add_description(parser)
    assert (
        description == "## Description\n\nA simple file copy script.\n\n"
    ), "Description should be added to the markdown"


def test_add_overall_usage(parser):
    expected_usage = (
        "## Overall Usage Example\n\n`script.py -s <source_path> -d <dest_path>"
        " [-v]`\n\n"
    )
    usage = _add_overall_usage(parser)
    assert usage == expected_usage, "Overall usage should be added to the markdown"


def test_add_table_of_contents(parser):
    contents = _add_table_of_contents(parser)
    assert "- [source](#source)" in contents
    assert "- [destination](#destination)" in contents
    assert "- [verbose](#verbose)" in contents


def test_document_action(parser):
    for action in parser._actions:
        if action.dest == "help":
            continue

        expected_flags = f"**Flags**: `{', '.join(action.option_strings)}`\n\n"
        expected_required = f"**Required**: {'Yes' if action.required else 'No'}\n\n"

        if action.metavar:
            if action.option_strings:
                cmd_example = f"{action.option_strings[0]} <{action.metavar}>"
            else:
                cmd_example = action.metavar
            expected_usage = f"#### Example Usage\n\n`{cmd_example}`\n"
        else:
            expected_usage = ""

        documentation = _document_action(action)

        assert f"### {action.dest}\n\n" in documentation
        assert f"{action.help}\n\n" in documentation
        assert expected_flags in documentation
        assert expected_required in documentation
        assert expected_usage in documentation
