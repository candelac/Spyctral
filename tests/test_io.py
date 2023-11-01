#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import pytest
import os
from spyctral import io  # read_fisa


from pathlib import Path


PATH = Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "Add_on"


@pytest.fixture(scope="session")
def data_path():
    return TEST_DATA_PATH.joinpath


# Definición de los casos de prueba parametrizados


@pytest.mark.parametrize(
    "input_file, exp_version, exp_reddening, exp_NP, exp_template",
    [
        (
            "fisa_1.fisa",
            "0.91",
            0.123868769,
            3299.45020,
            "/home/juan_test_1/FISA/templates/G1.dat",
        ),
        (
            "fisa_2.fisa",
            "0.92",
            0.234868769,
            7799.45020,
            "/home/test_2/FISA/templates/G2.dat",
        ),
        (
            "fisa_3.fisa",
            "0.93",
            0.330868769,
            3399.45020,
            "/home/test_3/FISA/templates/G3.dat",
        ),
        (
            "fisa_4.fisa",
            "0.94",
            0.440868769,
            4499.45020,
            "/home/test_4/FISA/templates/G4.dat",
        ),
    ],
)
def test_read_fisa_parametrized(
    input_file,
    exp_version,
    exp_reddening,
    exp_NP,
    exp_template,
):
    # Crea un archivo de prueba con contenido específico
    tmp_path = os.getcwd() + "/fisa_files/"
    test_file = tmp_path + input_file
    summary = read_fisa(test_file)

    assert summary.header["fisa_version"] == exp_version
    assert summary.header["reddening"] == exp_reddening
    assert summary.header["normalization_point"] == exp_NP
    assert summary.header["adopted_template"] == exp_template
    # Agregar más aserciones según sea necesario
