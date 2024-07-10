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

import numpy as np

import pytest

from specutils import Spectrum1D

from spyctral.core import core
from spyctral.io import fisa
from spyctral.utils.bunch import Bunch


# =============================================================================
# FISA TESTS
# =============================================================================


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

    assert isinstance(summary.data, Bunch)
    assert isinstance(summary.data.Unreddened_spectrum, QTable)
    assert isinstance(summary.data.Template_spectrum, QTable)
    assert isinstance(summary.data.Observed_spectrum, QTable)
    assert isinstance(summary.data.Residual_flux, QTable)

    assert len(summary.data.Unreddened_spectrum) == 3000
    assert len(summary.data.Template_spectrum) == 3401
    assert len(summary.data.Observed_spectrum) == 3000
    assert len(summary.data.Residual_flux) == 3000

    assert isinstance(summary.age, float)
    assert isinstance(summary.reddening, float)
    assert isinstance(summary.av_value, float)
    assert isinstance(summary.normalization_point, float)
    assert isinstance(summary.z_value, float)

    assert isinstance(summary.spectra, Bunch)
    assert isinstance(summary.spectra.Unreddened_spectrum, Spectrum1D)
    assert isinstance(summary.spectra.Template_spectrum, Spectrum1D)
    assert isinstance(summary.spectra.Observed_spectrum, Spectrum1D)
    assert isinstance(summary.spectra.Residual_flux, Spectrum1D)

    assert isinstance(summary.extra_info, Bunch)
    assert isinstance(summary.extra_info.str_template, str)
    assert isinstance(summary.extra_info.name_template, str)
    assert isinstance(summary.extra_info.age_map, dict)
    assert isinstance(summary.extra_info.z_map, dict)

    assert summary.extra_info.str_template == "G2.dat"
    assert summary.extra_info.name_template == "G2"
    assert (
        summary.age
        == summary.extra_info.age_map[summary.extra_info.name_template]
    )
    assert (
        summary.z_value
        == summary.extra_info.z_map[summary.extra_info.name_template]
    )


def test_read_fisa_with_nodefault_parameters(file_path):
    """Test FISA with no-default parameters"""
    path = file_path("case_SC_FISA.fisa")
    age_map_test = {
        "G1": np.random.randint(1e6, 1e12),
        "G3": np.random.randint(1e6, 1e12),
    }
    z_map_test = {
        "G1": np.random.randint(-1, 1),
        "G3": np.random.randint(-1, 1),
    }

    with pytest.raises(
        ValueError, match="Missing age mapping for template 'G2' in age_map."
    ):
        fisa.read_fisa(path, age_map=age_map_test)

    with pytest.raises(
        ValueError,
        match="Missing metallicity mapping for template 'G2' in z_map.",
    ):
        fisa.read_fisa(path, z_map=z_map_test)
