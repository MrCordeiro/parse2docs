import importlib
import os
import sys
from pathlib import Path
from types import ModuleType


def get_module_from_path(path: str) -> ModuleType:
    """Import a Python module from a given path."""
    module_name = _get_module_name(path)
    module_name = Path(path).stem
    with SysPathContext(path):
        return importlib.import_module(module_name)


def _get_module_name(path: str) -> str:
    module_name = path.replace("/", ".").replace("\\", ".")
    if module_name.endswith(".py"):
        module_name = module_name[:-3]
    return module_name


class SysPathContext:
    """Context manager that temporarily adds a given path to the sys.path."""

    def __init__(self, path: str):
        self.script_dir = os.path.dirname(os.path.abspath(path))
        self.old_path = sys.path.copy()

    def __enter__(self):
        sys.path.insert(0, self.script_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.path = self.old_path
