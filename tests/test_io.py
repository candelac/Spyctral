#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

"""Test input data."""

# =============================================================================
# IMPORTS
# =============================================================================

import os
from pathlib import Path

from spyctral import core, io


PATH = Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "Add_on"


def test_read_fisa():
    path = TEST_DATA_PATH / "case_SC_FISA.fisa"

    summary = io.read_fisa(path)

    assert isinstance(summary, core.SpectralSummary) is True

    assert summary.header.fisa_version == "0.92"
    # assert summary.header.date_time == datetime.datetime(
    #    2022, 4, 1, 21, 46, 19
    # )
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
