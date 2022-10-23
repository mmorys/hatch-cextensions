#!/usr/bin/env python3

from distutils.core import Extension
from distutils.core import setup


setup(
    name="helloworld",
    version="1.0",
    ext_modules=[Extension("helloworld", ["bind.c", "libmypy.c"])],
)
