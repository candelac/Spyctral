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

# import datetime as dt

# from astropy.table import QTable

# import pandas as pd

# from spyctral import core

# from spyctral.io import fisa

# from spyctral.utils.bunch import Bunch


# def test_spectralsummary_header_info_df(file_path):
#    path = file_path("case_SC_FISA.fisa")
#
#    summary = fisa.read_fisa(path)
#
#    df = summary.header_info_df
#
#    df_expected = pd.DataFrame(
#        {
#            0: [
#                "0.92",
#                "2022-04-01 21:46:19",
#                0.280869,
#                "/home/federico/FISA/templates/G2.dat",
#                5299.4502,
#                "(Unreddened_spectrum, Template_spectrum, Observed_spectrum)",
#            ]
#        },
#        index=[
#            "fisa_version",
#            "date_time",
#            "reddening",
#            "adopted_template",
#            "normalization_point",
#            "spectra_names",
#        ],
#    )
# pd.DataFrame(
#    {
#        "fisa_version": 0,
#        "date_time": "2022-04-01 21:46:19",
#        "reddening": 0.280869,
#        "adopted_template": "/home/federico/FISA/templates/G2.dat",
#        "normalization_point": 5299.4502,
#        "spectra_names": "(Unreddened_spectrum,
# Template_spectrum, Obser...",
#    }
# )

# df = header.header_info_df()

# assert df.equals(df_expected)
