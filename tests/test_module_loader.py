import sys
from pathlib import Path

from parse2docs.module_loader import SysPathContext, get_module_from_path


def test_sys_path_context():
    original_sys_path = sys.path.copy()
    test_file_path = Path(__file__).resolve()
    test_script_dir = str(test_file_path.parent)

    with SysPathContext(test_file_path):
        assert sys.path[0] == test_script_dir, (
            "When entering the context, the first entry in sys.path should be the "
            "parent directory"
        )

    assert (
        sys.path == original_sys_path
    ), "When leaving the context, sys.path should be restored to its original state"


def test_get_module_from_path():
    # Test importing a module from a path
    demo_module_path = Path(__file__).parent / "demo_parser_in_module.py"
    demo_module = get_module_from_path(demo_module_path)
    assert hasattr(demo_module, "main")
