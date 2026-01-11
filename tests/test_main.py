import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_module_importable():
    import main  # noqa: F401
