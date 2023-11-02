#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# DOCS
# =============================================================================

"""
Spyctral.

Implementation of astronomical objects spectral analisys.
"""

# =============================================================================
# META
# =============================================================================

__version__ = "0.1"


# =============================================================================
# IMPORTS
# =============================================================================

from .core import SpectralSummary
from .io import read_fisa


__all__ = [
    "SpectralSummary",
    "read_fisa",
]


# __file__ ?
