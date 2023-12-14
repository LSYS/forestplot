#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for PyPI."""
from setuptools import setup

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

install_requires = ["pandas", "numpy", "matplotlib", "matplotlib-inline<=0.1.3"]
setup(
    name="forestplot",
    version="0.3.2",
    license="MIT",
    author="Lucas Shen",
    author_email="lucas@lucasshen.com",
    maintainer="Lucas Shen",
    maintainer_email="lucas@lucasshen.com",
    url="https://github.com/lsys/forestplot",
    description="A Python package to make publication-ready but customizable forest plots.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=["forestplot"],
    install_requires=install_requires,
    keywords=[
        "visualization",
        "python",
        "data-science",
        "dataviz",
        "pandas",
        "matplotlib",
        "mpl",
        "forestplot",
        "blobbogram",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
