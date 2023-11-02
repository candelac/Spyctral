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
    header = attrs.field(converter=lambda v: Bunch("header_items:", v))
    data = attrs.field(converter=lambda v: Bunch("data_items:", v))
