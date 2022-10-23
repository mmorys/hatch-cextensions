import os
from contextlib import contextmanager

import pytest

from .utils import copy_directory_from_examples
from .utils import examples_list


@pytest.fixture(scope="session", params=examples_list())
def project_path(tmp_path_factory, request):
    temporary_dir = tmp_path_factory.mktemp("hatch_cextensions_tmp", numbered=True)
    with create_project(temporary_dir, request.param) as project:
        yield project


@contextmanager
def create_project(directory, project_name):
    temp_project_dir = os.path.join(directory, project_name)
    copy_directory_from_examples(project_name, temp_project_dir)

    origin = os.getcwd()
    os.chdir(temp_project_dir)
    try:
        yield temp_project_dir
    finally:
        os.chdir(origin)
