import sys
from argparse import Action, ArgumentParser, FileType
from pathlib import Path


def generate_markdown(parser: ArgumentParser) -> str:
    """Generate markdown from argparse object.

    Args:
        parser (ArgumentParser): argparse.ArgumentParser object.

    Returns:
        str: A string of the usage documentation in Markdown format.
    """
    markdown_string = "# Usage Documentation\n\n"
    markdown_string += _add_description(parser)
    markdown_string += _add_overall_usage(parser)
    markdown_string += _add_table_of_contents(parser)

    action_docs = [
        _document_action(action) for action in parser._actions if action.dest != "help"
    ]
    if action_docs:
        markdown_string += "## Options\n\n"

    markdown_string += "".join(action_docs)

    return markdown_string


def _add_description(parser) -> str:
    return f"## Description\n\n{parser.description}\n\n"


def _add_table_of_contents(parser: ArgumentParser) -> str:
    contents = "## Table of Contents\n\n"
    for action in parser._actions:
        if action.dest == "help":
            continue
        contents += f"- [{action.dest}](#{action.dest})\n"
    contents += "\n"
    return contents


def _document_action(action: Action) -> str:
    doc = f"### {action.dest}\n\n"
    doc += f"{action.help}\n\n"

    if action.option_strings:
        doc += f"**Flags**: `{', '.join(action.option_strings)}`\n\n"

    if isinstance(action.type, FileType):
        doc += "**Type**: `file` \n\n"
    elif action.type:
        doc += f"**Type**: `{action.type.__name__}`\n\n"

    doc += "**Required**: Yes\n\n" if action.required else "**Required**: No\n\n"

    # Add example usage
    if action.metavar:
        if action.option_strings:
            cmd_example = f"{action.option_strings[0]} <{action.metavar}>"
        else:
            cmd_example = action.metavar
        doc += f"#### Example Usage\n\n`{cmd_example}`\n"

    return doc


def _add_overall_usage(parser: ArgumentParser) -> str:
    cmd_example = []
    for action in parser._actions:
        # When the action doesn't have any option strings, it's a positional
        # argument
        if not action.option_strings:
            cmd_example.append(f"<{action.dest}>")
            continue

        # Skip help flag
        if action.option_strings[0] == "-h":
            continue

        value = _get_example_value_from_action(action)

        # Include brackets for optional arguments
        if action.required:
            cmd_example.append(f"{action.option_strings[0]}{value}")
        else:
            cmd_example.append(f"[{action.option_strings[0]}{value}]")

    cmd_example = " ".join(cmd_example)
    script_name = _get_script_name()

    if cmd_example.strip() == "":
        return f"## Overall Usage Example\n\n`{script_name}`\n\n"

    return f"## Overall Usage Example\n\n`{script_name} {cmd_example}`\n\n"


def _get_script_name() -> str:
    # Running from the command line, so the script name is the last argument
    if "parse2docs" in sys.argv:
        return Path(sys.argv[-1]).name

    # When running from a module, the script name is the module name
    return Path(__file__).name


def _get_example_value_from_action(action: Action) -> str:
    if action.metavar:
        value = f" <{action.metavar}>"
    elif action.nargs == 0:
        value = ""
    else:
        value = " <value>"
    return value
