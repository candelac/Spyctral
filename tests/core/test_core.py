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

import numpy as np

import pandas as pd

import pytest

from spyctral.io import fisa
from spyctral.utils.bunch import Bunch


# =============================================================================
# CONSTANTS
# =============================================================================

#: Z sun (cite)
Z_SUN = 0.019


# =============================================================================
# SpectralSummary TESTS
# =============================================================================


def test_spectralsummary_header_info_df(file_path):
    """Test of the "header_info_df" property with FISA."""

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


def test_spectralsummary_get_spectrum(file_path):
    """Test of the "get_spectrum" with FISA."""

    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    observed_spectrum = summary.get_spectrum("Observed_spectrum")
    expected_spectrum = summary.spectra["Observed_spectrum"]

    assert observed_spectrum.flux.unit == expected_spectrum.flux.unit
    assert (
        observed_spectrum.wavelength.unit == expected_spectrum.wavelength.unit
    )

    assert np.allclose(
        observed_spectrum.flux.value, expected_spectrum.flux.value
    )
    assert np.allclose(
        observed_spectrum.wavelength.value, expected_spectrum.wavelength.value
    )


def test_spectralsummary_getitem(file_path):
    """Test of the header "__getitem__" with FISA."""

    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    header_expected = Bunch(
        "header",
        {
            "fisa_version": "0.92",
            "normalization_point": 5299.4502,
            "spectra_names": (
                "Unreddened_spectrum",
                "Template_spectrum",
                "Observed_spectrum",
                "Residual_flux",
            ),
            "adopted_template": "/home/federico/FISA/templates/G2.dat",
            "date_time": dateutil.parser.parse("04/01/2022 21:46:19"),
            "reddening": 0.280868769,
        },
    )

    assert summary["header"] == header_expected
    # assert summary["data"] == data_expected
    assert summary["age"] == 9.0
    assert summary["reddening"] == 0.280868769
    assert summary["av_value"] == 0.8706931839000001
    assert summary["normalization_point"] == 5299.4502
    assert summary["z_value"] == 0.4
    # assert summary["extra_info"] == extra_info_expected


def test_spectralsummary_bad_getitem(file_path):
    """Test of the "__getitem__" with with a nonexistent attribute."""

    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    with pytest.raises(KeyError):
        _ = summary["nonexistent_attribute"]


def test_spectralsummary_len(file_path):
    """Test of the "__len__" with FISA."""

    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    assert len(summary) == 9
    assert len(summary.header) == 6
    assert len(summary.data) == 4
    assert len(summary.extra_info) == 4


def test_spectralsummary_repr(file_path):
    """Test of the "__repr__" with FISA."""

    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    repr_expected = (
        "SpectralSummary(\n"
        "  header={fisa_version, date_time, reddening,"
        " adopted_template, normalization_point, spectra_names},\n"
        "  data={Unreddened_spectrum, Template_spectrum, Observed_spectrum,"
        " Residual_flux},\n"
        "  age, reddening, av_value, normalization_point, z_value,\n"
        "  spectra={Unreddened_spectrum, Template_spectrum, Observed_spectrum,"
        " Residual_flux},\n"
        "  extra_info={str_template, name_template, age_map, z_map})"
    )

    assert repr(summary) == repr_expected


def test_spectralsummary_feh_ratio(file_path):
    """Test of the "feh_ratio" with FISA."""

    path = file_path("case_SC_FISA.fisa")

    summary = fisa.read_fisa(path)

    feh_ratio_expected = np.log10(summary.z_value / Z_SUN)

    assert summary.feh_ratio == feh_ratio_expected
