#!/usr/bin/env python
"""
======
pyczmq
======
"""
from pyczmq.zmq import version as zmq_version
from pyczmq.zsys import zsys_version as czmq_version
from setuptools import setup, find_packages
import sys


if zmq_version() < (4,0,0) or czmq_version() < (2, 1, 0):
    print "ERROR: pyczmq requires libzmq 4.0.0 or later and libczmq 2.1.0 or later"
    sys.exit(1)


setup(
  name="pyczmq",
  version="0.0.4",
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
