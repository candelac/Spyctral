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

from astropy.table import QTable

import pytest

from spyctral import io


PATH = Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "Add_on"


# Definición de los casos de prueba parametrizados


@pytest.mark.parametrize(
    "input_file, exp_ver, exp_red, exp_np, exp_temp, tab_names",
    [
        (
            "fisa_1.fisa",
            "0.91",
            0.123868769,
            3299.45020,
            "/home/juan_test_1/FISA/templates/G1.dat",
            (
                "Unreddened_spect",
                "Template_spectrum",
                "Observed_sp",
                "Residual_flux",
                "xxx_flux",
            ),
        ),
        (
            "fisa_2.fisa",
            "0.92",
            0.234868769,
            7799.45020,
            "/home/test_2/FISA/templates/G2.dat",
            (
                "Unreddened_spectrum",
                "Blue_spectrum",
                "Template_spectrum",
                "Observed_spectrum",
                "Residual_flux",
            ),
        ),
        (
            "fisa_3.fisa",
            "0.93",
            0.330868769,
            3399.45020,
            "/home/test_3/FISA/templates/G3.dat",
            (
                "Unreddened_spectrum",
                "Template_spectrum",
                "Observed_spectrum",
                "Residual_flux",
            ),
        ),
        (
            "fisa_4.fisa",
            "0.94",
            0.440868769,
            4499.45020,
            "/home/test_4/FISA/templates/G4.dat",
            (
                "Unreddened_spectrum",
                "Template_spectrum",
                "Observed_spectrum",
                "Residual_flux",
                "test_spectrum_1",
                "test_spectrum_2",
            ),
        ),
    ],
)
def test_process_header(
    input_file, exp_ver, exp_red, exp_np, exp_temp, tab_names
):
    # Crea un archivo de prueba con contenido específico
    path = TEST_DATA_PATH / input_file
    summary = io.read_fisa(path)

    assert summary.header["fisa_version"] == exp_ver
    assert summary.header["reddening"] == exp_red
    assert summary.header["normalization_point"] == exp_np
    assert summary.header["adopted_template"] == exp_temp
    assert tuple(summary.data.keys()) == tab_names
    # Agregar más aserciones según sea necesario


def test_fisa_spectra_names():
    # Creo los datos para las QTables

    data = [
        [[1, 2], [3, 4], [5, 6]],
        [[7, 8], [9, 10], [11, 12]],
        [[13, 14], [15, 16], [17, 18]],
        [[19, 20], [21, 22], [23, 24]],
    ]
    table_names = (
        "Unreddened_spectrum",
        "Template_spect",
        "Observed_spec",
        "Residual_flux",
    )
    spectra = [
        QTable(rows=d, names=("Wavelength", "Normalizated_flux")) for d in data
    ]

    exp_results = {
        "Unreddened_spectrum": spectra[0],
        "Template_spect": spectra[1],
        "Observed_spec": spectra[2],
        "Residual_flux": spectra[3],
    }

    renamed_spectra = io._fisa_spectra_names(spectra, table_names)

    assert renamed_spectra == exp_results
