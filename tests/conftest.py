# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import errno
import os
import shutil
import stat
import tempfile
from contextlib import contextmanager

import pytest

from .utils import copy_directory_from_examples, examples_list


def handle_remove_readonly(func, path, exc):  # no cov
    # PermissionError: [WinError 5] Access is denied: '...\\.git\\...'
    if func in (os.rmdir, os.remove, os.unlink) and exc[1].errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        func(path)
    else:
        raise


@pytest.fixture
def temp_dir():
    directory = tempfile.mkdtemp()
    try:
        directory = os.path.realpath(directory)
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)


@contextmanager
def create_project(directory, project_name):
    project_dir = os.path.join(directory, project_name)
    copy_directory_from_examples(project_name, project_dir)

    origin = os.getcwd()
    os.chdir(project_dir)
    try:
        yield project_dir
    finally:
        os.chdir(origin)


@pytest.fixture(params=examples_list())
def new_project(temp_dir, request):
    with create_project(temp_dir, request.param) as project:
        yield project
