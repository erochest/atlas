#! /usr/bin/env python


from distutils.core import setup, Extension
import os

setup(
    name='lap',
    version='0.1a2',
    description='Linguistic Atlas Projects utilities',
    author='Eric Rochester',
    author_email='erochest@uga.edu',
    url='http://us.english.uga.edu/new/utils/',

    packages=[
        'lap',
        'lap.data',
        'lap.test',
        'lap.web',
        'lap.web.templates',
        ],
    ext_modules=[
        Extension('lap.data._lamcour',
                  [os.path.join('lap', 'data', '_lamcour.c')]),
        #Extension('lap.data.fcsv', [
        #    os.path.join('lap', 'data', 'fcsv.c'),
        #    os.path.join('lap', 'data', 'fcsvmem.c'),
        #    os.path.join('lap', 'data', 'fcsvmodule.c'),
        #    ]),
        ],
    scripts=[os.path.join('scripts', 'csv2db.py')],
    data_files=[('lap-tools', [os.path.join('scripts', 'buildsite.py')])],
    )

