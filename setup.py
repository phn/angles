#!/usr/bin/env python

from distutils.core import setup

import angles

version = angles.__version__

description = """\
Classes for representing angles, and positions on a unit sphere."""

long_description = open("README.rst").read()

setup(
    name="angles",
    version=version,
    description=description,
    long_description=long_description,
    license='BSD',
    author="Prasanth Nair",
    author_email="prasanthhn@gmail.com",
    url='http://github.com/phn/angles',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Programming Language :: Python',
        ],
    py_modules=["angles"]
    )
