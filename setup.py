#!/usr/bin/env python
from setuptools import setup

setup(
    name="irator",
    version='0.2.0',
    author='Jaiko',
    description="A Twisted-friendly Client for IRE's Irator API.",
    url="https://github.com/spicerack/irator",
    py_modules= ['irator',],
    install_requires=['twisted', 'requests']
)