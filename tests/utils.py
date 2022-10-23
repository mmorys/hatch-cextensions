import os
import pathlib
import shutil
import subprocess  # noqa: S404
import sys


def examples_list():
    return [exmpl.name for exmpl in _examples_path().iterdir() if exmpl.is_dir() and not exmpl.name.startswith(".")]


def _examples_path():
    return pathlib.Path(__file__).parent.joinpath("examples")


def copy_directory_from_examples(src_dir, dst_path):
    src_path_absolute = _examples_path().joinpath(src_dir).resolve()
    print(src_path_absolute)
    dst_path_absolute = pathlib.Path(dst_path).resolve()
    print(dst_path_absolute)
    shutil.copytree(src_path_absolute, dst_path_absolute)


def build_project(*args, **kwargs):
    env = kwargs.get("env", os.environ.copy())
    _run_command(sys.executable, "-m", "hatchling", "build", *args, env=env)


def _run_command(*command, **kwargs):  # sourcery skip: raise-specific-error
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)  # noqa: S603
    stdout, _ = process.communicate()

    if process.returncode:  # no cov
        raise Exception(stdout.decode("utf-8"))
