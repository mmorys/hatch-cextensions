import os
import pathlib
import shutil
import subprocess
import sys


def _examples_path():
    return pathlib.Path(__file__).parent.joinpath("examples")


def examples_list():
    return [exmpl for exmpl in _examples_path().iterdir() if exmpl.is_dir() and not exmpl.name.startswith(".")]


def copy_directory_from_examples(src_dir, dst_path):
    src_path_absolute = _examples_path().joinpath(src_dir).resolve()
    print(src_path_absolute)
    dst_path_absolute = pathlib.Path(dst_path).resolve()
    print(dst_path_absolute)
    shutil.copytree(src_path_absolute, dst_path_absolute)


def create_file(path):
    with open(path, "a"):
        os.utime(path, None)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_file(path, contents):
    with open(path, "w") as f:
        f.write(contents)


def build_project(*args, **kwargs):
    if "env" not in kwargs:
        env = os.environ.copy()
        env.pop("SETUPTOOLS_SCM_PRETEND_VERSION", None)
    else:
        env = kwargs["env"]
    _run_command(sys.executable, "-m", "hatchling", "build", *args, env=env)


def _run_command(*command, **kwargs):  # sourcery skip: raise-specific-error
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
    stdout, _ = process.communicate()

    if process.returncode:  # no cov
        raise Exception(stdout.decode("utf-8"))
