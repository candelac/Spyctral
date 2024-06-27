# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

"""Test input core."""

# =============================================================================
# IMPORTS
# =============================================================================


import dateutil.parser

import pandas as pd

from spyctral.io import fisa


def test_header_info_df(file_path):
    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    df = summary.header_info_df

    df_expected = pd.DataFrame(
        {
            "value": [
                "0.92",
                dateutil.parser.parse("04/01/2022 21:46:19"),
                0.280868769,
                "/home/federico/FISA/templates/G2.dat",
                5299.4502,
                (
                    "Unreddened_spectrum",
                    "Template_spectrum",
                    "Observed_spectrum",
                    "Residual_flux",
                ),
            ]
        },
        index=[
            "fisa_version",
            "date_time",
            "reddening",
            "adopted_template",
            "normalization_point",
            "spectra_names",
        ],
    )

    assert df.equals(df_expected)
