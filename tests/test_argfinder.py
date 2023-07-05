from argparse import ArgumentParser
from types import ModuleType

import pytest

from parse2docs.argfinder import get_argparser_from_module

from . import demo_parser_in_function, demo_parser_in_module


def test_find_argparser_in_module():
    assert isinstance(get_argparser_from_module(demo_parser_in_module), ArgumentParser)


def test_find_argparser_in_functions():
    assert isinstance(
        get_argparser_from_module(demo_parser_in_function), ArgumentParser
    )


def testget_argparser_from_module_no_parser():
    empty_module = ModuleType("empty_module", "Empty test module")
    with pytest.raises(ValueError):
        get_argparser_from_module(empty_module)
