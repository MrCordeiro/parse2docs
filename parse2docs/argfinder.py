"""Module for finding ArgumentParser objects in Python scripts."""

import inspect
from argparse import ArgumentParser
from types import ModuleType


def get_argparser_from_module(module: ModuleType) -> ArgumentParser:
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

    search_functions = [_find_parser_in_scope, _find_parser_in_functions]
    parser = next((func(module) for func in search_functions if func(module)), None)

    if parser is None:
        raise ValueError("No ArgumentParser object found in the provided file.")

    return parser


def _find_parser_in_scope(module: ModuleType) -> ArgumentParser | None:
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, ArgumentParser):
            return obj


def _find_parser_in_functions(module: ModuleType) -> ArgumentParser | None:
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
