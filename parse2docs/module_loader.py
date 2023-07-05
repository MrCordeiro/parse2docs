import importlib
import sys
from pathlib import Path
from types import ModuleType


def get_module_from_path(path: Path) -> ModuleType:
    """Import a Python module from a given path."""
    module_name = path.stem
    with SysPathContext(path):
        return importlib.import_module(module_name)


class SysPathContext:
    """Context manager that temporarily adds a given path to the sys.path."""

    def __init__(self, path: Path):
        self.script_dir = path.parent.absolute()
        self.old_path = sys.path.copy()

    def __enter__(self):
        sys.path.insert(0, str(self.script_dir))

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.path = self.old_path
