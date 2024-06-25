# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

"""FISA test input data."""

# =============================================================================
# IMPORTS
# =============================================================================

import datetime as dt

from astropy.table import QTable

from spyctral import core
from spyctral.io import fisa
from spyctral.utils.bunch import Bunch


def test_read_fisa(file_path):
    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    assert isinstance(summary, core.SpectralSummary)

    assert isinstance(summary.header, Bunch)
    assert isinstance(summary.header.fisa_version, str)
    assert isinstance(summary.header.reddening, float)
    assert isinstance(summary.header.date_time, dt.datetime) is True
    assert isinstance(summary.header.adopted_template, str)
    assert isinstance(summary.header.normalization_point, float)
    assert isinstance(summary.header.spectra_names, tuple)

    assert isinstance(summary.data, Bunch)
    assert isinstance(summary.data.Unreddened_spectrum, QTable)
    assert isinstance(summary.data.Template_spectrum, QTable)
    assert isinstance(summary.data.Observed_spectrum, QTable)
    assert isinstance(summary.data.Residual_flux, QTable)

    assert summary.header.fisa_version == "0.92"
    assert summary.header.date_time == dt.datetime(2022, 4, 1, 21, 46, 19)
    assert summary.header.reddening == 0.280868769
    assert (
        summary.header.adopted_template
        == "/home/federico/FISA/templates/G2.dat"
    )
    assert summary.header.normalization_point == 5299.4502
    assert summary.header.spectra_names == (
        "Unreddened_spectrum",
        "Template_spectrum",
        "Observed_spectrum",
        "Residual_flux",
    )

    assert len(summary.data.Unreddened_spectrum) == 3000
    assert len(summary.data.Template_spectrum) == 3401
    assert len(summary.data.Observed_spectrum) == 3000
    assert len(summary.data.Residual_flux) == 3000

    assert isinstance(summary.age, float)
    assert summary.age == 1e9

    assert isinstance(summary.reddening, float)
    assert isinstance(summary.av_value, float)
    assert isinstance(summary.normalization_point, float)
    assert isinstance(summary.z_value, float)
    assert isinstance(summary.extra_info, Bunch)
