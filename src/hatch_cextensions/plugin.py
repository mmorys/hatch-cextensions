import os
import shutil
import subprocess  # noqa: S404
import sys
import uuid
from contextlib import contextmanager
from contextlib import suppress

from hatchling.builders.hooks.plugin.interface import BuildHookInterface  # pyright: ignore[reportMissingImports]


class PythonBuildExtensionError(Exception):
    pass


class CExtensionBuildHook(BuildHookInterface):
    """Provides hook to run before Hatch package build to compile C Extensions using setuptools."""

    PLUGIN_NAME = "cextension"

    @contextmanager
    def _hide_project_file(self):
        # TODO: remove this and bump setuptools when it supports PEP 639
        unique_value = uuid.uuid4().hex
        project_file = os.path.join(self.root, "pyproject.toml")
        project_file_backup = os.path.join(self.root, f"pyproject.toml.bak{unique_value}")

        os.replace(project_file, project_file_backup)
        try:
            yield
        finally:
            os.replace(project_file_backup, project_file)

    def clean(self, versions):
        with suppress(FileNotFoundError):
            shutil.rmtree("build")
        with suppress(FileNotFoundError):
            os.remove("setup.py")
        for file_name in os.listdir(self._src_dir):
            if file_name.endswith(("_wrap.cpp", ".py") + self._library_extensions()):
                os.remove(os.path.join(self._src_dir, file_name))

    @contextmanager
    def _setup_py(self):
        ext_sources = [
            os.path.join(self._src_dir, file_name)
            for file_name in os.listdir(self._src_dir)
            if file_name.endswith((".i", ".cpp"))
        ]

        setup_py_contents = f"""\
from setuptools import setup, Extension

custom_extension = Extension(name='src._{self._package_name}',
                        sources={ext_sources},
                        include_dirs=['{self._src_dir}'],
                        language='c++',
                        swig_opts=['-c++']
                        )

setup(
    ext_package='{self._package_root}',
    ext_modules=[midas_module]
)
"""
        setup_py_path = os.path.join(self.root, "setup.py")
        try:
            with open(setup_py_path, "w", encoding="utf-8") as f:
                f.write(setup_py_contents)
            yield setup_py_path
        finally:
            os.remove(setup_py_path)

    def initialize(self, version, build_data):
        if self.target_name != "wheel":
            return

        with self._hide_project_file():
            with self._setup_py() as setup_file:
                process = subprocess.run(  # noqa: S603
                    [sys.executable, setup_file, "build_ext", "--inplace"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
        if process.returncode:  # no cov
            raise PythonBuildExtensionError(f'Error while invoking Swig:\n{process.stdout.decode("utf-8")}')

        build_data["infer_tag"] = True
        build_data["pure_python"] = False
        build_data["artifacts"].extend(self._build_artifacts)
