#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# Copiado de feets, y comentado lo que creo que hace cada funcion
# saque lo que creo que no iria en nuestro caso

# =============================================================================
# DOC
# =============================================================================

""""""


# =============================================================================
# IMPORTS
# =============================================================================

from .core import Extractor


# =============================================================================
# EXTRACTOR CLASS
# =============================================================================


class AgeFisa(Extractor):
    """
    **Age**

    explicacion de lo que calcula y como

    """

    data = ["fisa"]

    features = ["Age"]

    def fit(self, fisa):
        template = fisa.header.adopted_template
        age = template.split("/")[-1]

        return {"Age": age}
