#!/usr/bin/env python
"""
======
pyczmq
======
"""
from setuptools import setup, find_packages

setup(
  name="pyczmq",
  version="3.0.0",
  packages=find_packages(exclude=['tests.*', 'tests', '.virt']),

  tests_require=['nose'],
  test_suite='nose.collector',

  author='Michel Pelletier',
  author_email='pelletier.michel@yahoo.com',
  description='pyczmq cffi wrapper',
  long_description=__doc__,
  license='MIT License',
  url='https://github.com/michelp/pyczmq',
      install_requires=[
        'cffi',
        ],
  classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        ],
)
