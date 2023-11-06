#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.
import os
from pathlib import Path

from astropy.table import QTable

from spyctral import core, io

PATH = Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "Add_on"

path = TEST_DATA_PATH / "fisa_1.fisa"

ss = io.read_fisa(path)
# print(ss.header)

print("tipo de objeto", type(ss))
print(type(ss.header.date_time))


class Test_SpectralSummary:  # (unittest.TestCase):
    def test_header(self):
        # Verificar que el campo 'header' sea igual al valor proporcionado
        # self.assertIn("fisa_version", ss.header)
        # self.assertIn("date_time", ss.header)
        # self.assertIn("spectra_names", ss.header)
        # self.assertIn("normalization_point", ss.header)
        # self.assertIn("adopted_template", ss.header)
        # self.assertIn("reddening", ss.header)
        assert "fisa_version" in ss.header
        assert "date_time" in ss.header
        assert "spectra_names" in ss.header
        assert "normalization_point" in ss.header
        assert "adopted_template" in ss.header
        assert "reddening" in ss.header

    def test_data(self):
        # self.assertEqual(len(ss.data.Unreddened_spectrum), 3000)
        # self.assertEqual(len(ss.data.Template_spectrum), 3401)
        # self.assertEqual(len(ss.data.Observed_spectrum), 3000)
        # self.assertEqual(len(ss.data.Residual_flux), 3000)
        assert len(ss.data.Unreddened_spectrum) == 3000
        assert len(ss.data.Template_spectrum) == 3401
        assert len(ss.data.Observed_spectrum) == 3000
        assert len(ss.data.Residual_flux) == 3000

    def test_type(self):
        assert isinstance(ss, core.SpectralSummary)
        assert isinstance(ss.data.Unreddened_spectrum, QTable)
        assert isinstance(ss.data.Template_spectrum, QTable)
        assert isinstance(ss.data.Observed_spectrum, QTable)
        assert isinstance(ss.data.Residual_flux, QTable)
        assert isinstance(ss.header.normalization_point, float)
        assert isinstance(ss.header.reddening, float)
        assert any("SpectralSummary")
        assert type(ss).__name__ == "SpectralSummary"
