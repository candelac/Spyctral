#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# DOCS
# =============================================================================

"""This file is for distribute and install Spyctral."""

# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

from setuptools import setup, find_packages

# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

REQUIREMENTS = ["attrs", "numpy", "python-dateutil"]

with open(PATH / "spyctral" / "__init__.py") as fp:
    for line in fp.readlines():
        if line.startswith("__version__"):
            VERSION = line.split("=", 1)[-1].replace('"', "").strip()
            break


with open("README.md") as fp:
    LONG_DESCRIPTION = fp.read()

DESCRIPTION = "Implementation of astronomical objects spectral analisys"

# =============================================================================
# FUNCTIONS
# =============================================================================

setup(
    name="spyctral",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Tapia-Reina M. I. et al",
    author_email="martina.tapia@mi.unc.edu.ar",
    url="https://github.com/candelac/Spyctral",
    packages=find_packages(),
    license="The MIT License",
    keywords=["spyctral", "spectra", "spectral-synthesis", "template-fitting"],
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=REQUIREMENTS,
)
