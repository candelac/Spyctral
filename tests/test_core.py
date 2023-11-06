#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.
import os
import sys
import unittest
from pathlib import Path

sys.path.append("/home/joseluis/Proyectos/")

from Spyctral.spyctral import io


PATH = Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "Add_on"

path = TEST_DATA_PATH / "fisa_1.fisa"

ss = io.read_fisa(path)
print(ss.header)

print(len(ss.data.Unreddened_spect))


class Test_SpectralSummary(unittest.TestCase):
    def test_header(self):
        # Verificar que el campo 'header' sea igual al valor proporcionado
        self.assertIn("fisa_version", ss.header)
        self.assertIn("date_time", ss.header)
        self.assertIn("spectra_names", ss.header)
        self.assertIn("normalization_point", ss.header)
        self.assertIn("adopted_template", ss.header)
        self.assertIn("reddening", ss.header)

    def test_data(self):
        self.assertEqual(len(ss.data.Unreddened_spect), 3000)
        self.assertEqual(len(ss.data.Template_spectrum), 3401)
        self.assertEqual(len(ss.data.Observed_sp), 3000)
        self.assertEqual(len(ss.data.Residual_flux), 3000)
        self.assertEqual(len(ss.data.xxx_flux), 3)


if __name__ == "__main__":
    unittest.main()
