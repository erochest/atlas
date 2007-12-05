#! /usr/bin/env python


from distutils.core import setup, Extension
import os

try:
    import py2exe
except ImportError:
    import warnings
    py2exe = None
    warnings.warn("py2exe not found. You won't be able to create executables.")


if py2exe:
    args = {
        console: [
            os.path.join('scripts', 'lamrecoder.py'),
            ],
        windows: [
            os.path.join('scripts', 'lamrec.py'),
            ],
        }
else:
    args = {}


setup(
    name='lamcour',
    version='0.0',
    description='lamcour encoding recoder',
    author='Eric Rochester',
    author_email='erochest@gmail.com',
    url='http://us.english.uga.edu/new/utils/',

    py_modules=[
        'lamcour',
        ],
    ext_modules=[
        Extension('_lamcour', ['_lamcour.c']),
        ],

    **args
    )

