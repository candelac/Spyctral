#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import attrs

from .utils.bunch import Bunch


@attrs.define
class SpectralSummary:
    data_in = attrs.field()
    header = attrs.field(converter=lambda v: Bunch("header", v))
