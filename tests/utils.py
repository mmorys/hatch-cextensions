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


def build_ext(*args, **kwargs):
    env = kwargs.get("env", os.environ.copy())
    _run_command(sys.executable, "-m", "hatchling", "build", *args, env=env)


def _run_command(*command, **kwargs):  # sourcery skip: raise-specific-error
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)  # noqa: S603
    stdout, _ = process.communicate()

    if process.returncode:  # no cov
        raise Exception(stdout.decode("utf-8"))


def file_exists(path):
    path = pathlib.Path(path)
    return path.exists() and path.is_file()


def directory_exists(path):
    path = pathlib.Path(path)
    return path.exists() and path.is_dir()


def content_with_prefix_exists(parent_dir, prefix, _type=None):
    # sourcery skip: reintroduce-else, remove-redundant-continue, use-next
    parent_dir = pathlib.Path(parent_dir)
    type_validators = {"file": "is_file", "dir": "is_dir", "directory": "is_directory"}
    for content in parent_dir.iterdir():
        if _type and not getattr(content, type_validators[_type])():
            continue
        if content.name.startswith(prefix):
            return True
    return False


def directory_with_prefix_exists(parent_dir, prefix):
    return content_with_prefix_exists(parent_dir, prefix, _type="dir")


def file_with_prefix_exists(parent_dir, prefix):
    return content_with_prefix_exists(parent_dir, prefix, _type="file")
