#!/usr/bin/env python
"""
======
pyczmq
======
"""
from setuptools import setup, find_packages

setup(
  name="pyczmq",
  version="0.0.2",
  packages=find_packages(exclude=['tests.*', 'tests', '.virt']),

  tests_require=['nose'],
  test_suite='nose.collector',

  author='Michel Pelletier',
  author_email='pelletier.michel@yahoo.com',
  description='pyczmq cffi wrapper',
  long_description=__doc__,
  license='LGPL v3',
  url='https://github.com/michelp/pyczmq',
      install_requires=[
        'cffi',
        ],
)
