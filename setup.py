#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    _globals = {}
    with open(os.path.join("fast_flow", "version.py")) as version_file:
        exec(version_file.read(), _globals)
    return _globals["__version__"]


setuptools.setup(
    name="fast-flow",
    version=get_version(),
    author="Ben Krikler",
    author_email="fast-hep@cern.ch",
    description="YAML-based analysis flow description language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fast-hep/fast-flow",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=['six', 'pyyaml'],
    #setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
    ),
)
