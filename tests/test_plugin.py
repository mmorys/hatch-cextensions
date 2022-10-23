import os
import pathlib


class TestProjectCreation:
    def test_tmp_proj_in_tmp(self, project_path):
        # TODO: find more secure means of addressing flake8-bandint error S108: Probable insecure usage of temp file/directory.
        assert os.getcwd().startswith("/tmp")  # noqa: S108

    def test_tmp_proj_files_copied(self, project_path):
        assert any(pth.name == "pyproject.toml" for pth in pathlib.Path(project_path).iterdir())

    def test_tmp_proj_dir_created(self, project_path):
        project = pathlib.Path(project_path)
        project_name = project.name
        toml_file = project.joinpath("pyproject.toml")
        with open(toml_file) as fid:
            assert project_name in fid.read()
