# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

"""Base objects and functions of Spyctral."""


# =============================================================================
# IMPORTS
# =============================================================================

from .core import SpectralSummary
from ..io.fisa import read_fisa
from ..io.starlight import read_starlight

__all__ = ["SpectralSummary", "read_fisa", "read_starlight"]


# __file__ ?
