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

import numpy as np

from .core import Extractor


# =============================================================================
# EXTRACTOR CLASS
# =============================================================================


class AgeStl(Extractor):
    """
    **Age**

    explicacion de lo que calcula y como

    """

    data = ["starlight"]

    features = ["Age"]

    params = {"n_aporte": 4, "n_decimales": 2}

    def _filter_ssp(self, starlight, n_aporte):
        # Tengo que filtrar antes de promediar
        # me quedo con las PES que aportan mas del n_aporte = 4% a la sintesis

        # voy a suponer que la tabla_synthesis_results se llama df
        # y es un dataframe

        df = starlight.tabla_synthesis_results
        df = df[df["x_j(%)"] > n_aporte]

        return df

    def fit(self, starlight, n_aporte, n_decimales):
        df = self._filter_ssp(starlight=starlight, n_aporte=n_aporte)
        age = int(
            10
            ** (
                ((df["x_j(%)"] * np.log10(df["age_j(yr)"]))).sum()
                / df["x_j(%)"].sum()
            )
        )
        age = np.log10(age)
        age = round(age, n_decimales)

        return {"Age": age}
