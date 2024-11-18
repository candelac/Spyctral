# !/usr/bin/env python
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

__version__ = "0.0.1"


# =============================================================================
# IMPORTS
# =============================================================================

from .core.core import SpectralSummary
from .core.plot import SpectralPlotter
from .io import fisa
from .io import starlight
from .io.fisa import read_fisa
from .io.starlight import read_starlight


__all__ = [
    "SpectralSummary",
    "fisa",
    "starlight",
    "read_fisa",
    "read_starlight",
    "SpectralPlotter",
]
