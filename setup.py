#! /usr/bin/env python


from distutils.core import setup, Extension
import os

setup(
    name='lamrecode',
    version='0.0',
    description='lamcour encoding recoder',
    author='Eric Rochester',
    author_email='erochest@gmail.com',
    url='http://us.english.uga.edu/new/utils/',

    packages=[
        'lamrecode',
        ],
    ext_modules=[
        Extension('lamrecode._lamcour', [os.path.join('lamrecode', '_lamcour.c')]),
        ],
    scripts=[],
    )

