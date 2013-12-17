#!/usr/bin/env python
"""
======
pyczmq
======
"""
from cffi import FFI
from setuptools import setup, find_packages
import sys

ffi = FFI()
Z = ffi.dlopen('zmq')
C = ffi.dlopen('czmq')

ffi.cdef('void zmq_version (int *major, int *minor, int *patch);')

def zmq_version(lib):
    """
    Returns the tuple (major, minor, patch) of the current libzmq version.
    """
    major = ffi.new('int*')
    minor= ffi.new('int*')
    patch = ffi.new('int*')
    Z.zmq_version(major, minor, patch)
    return (major[0], minor[0], patch[0])

zmq_version = zmq_version(Z)


if zmq_version < (4,0,0):
    print "ERROR: pyczmq requires libzmq 4.0.0 or later."
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
