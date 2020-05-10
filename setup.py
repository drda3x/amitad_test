#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="winner_app",
    version="0.0.1",
    test_suite="test",
    install_requires=['python-dateutil', 'flask'],
    packages=find_packages()
)
