#!/usr/bin/env python
from setuptools import setup

setup(
    name="irator",
    version='0.1.0',
    author='Jaiko',
    description="A Twisted-friendly Client for IRE's Irator API.",
    url="http://packages.python.org/an_example_pypi_project",
    py_modules= ['irator',],
    install_requires=['twisted']
)