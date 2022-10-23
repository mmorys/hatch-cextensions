import os


def test_setup_py_output(new_project):
    # from ..src.hatch_cextensions.plugin import CExtensionBuildHook

    # CExtensionBuildHook()
    assert os.getcwd().endswith("00-HelloWorld")
