# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

from astropy.table import QTable

import attrs

import pandas as pd

from specutils import Spectrum1D

from .utils.bunch import Bunch

# from plot_utils import make_plot_base


@attrs.define
class SpectralSummary:
    header = attrs.field(converter=lambda v: Bunch("header_items:", v))
    data = attrs.field(converter=lambda v: Bunch("data_items:", v))

    def __repr__(self):
        return (
            f"SpectralSummary(header={str(self.header)}, "
            f"data={str(self.data)})"
        )

    def header_to_dataframe(self):
        """Convert the header into a ``pandas.DataFrame``."""

        keys = list(self.header.keys())
        values = list(self.header.values())
        df = pd.DataFrame(values, index=keys)

        return df

    def data_to_separate_sets(self):
        """Create separate objects for each item in the data dictionary."""
        for key, value in self.data.items():
            setattr(self, key, value)

    def make_spectrum(self):
        """Create spectra from data"""
        self.data_to_separate_sets()  # Execute data_to_separate_sets
        spectra = {}
        for key, value in self.data.items():
            if isinstance(value, QTable):
                if len(value.columns) == 2:
                    try:
                        wavelength = value.columns[0]
                        flux = value.columns[1]
                        spectra[key] = Spectrum1D(
                            flux=flux, spectral_axis=wavelength
                        )
                    except IndexError as e:
                        print(f"Error creating spectrum for {key}: {e}")
                    except TypeError as e:
                        print(f"Error creating spectrum for {key}: {e}")
                elif len(value.columns) == 3:
                    try:
                        wavelength = value.columns[0]
                        flux_obs = value.columns[1]
                        flux_syn = value.columns[2]
                        residual_flux = (flux_obs - flux_syn) / flux_obs

                        spectra["synthetic_spectrum"] = Spectrum1D(
                            flux=flux_syn, spectral_axis=wavelength
                        )
                        spectra["observed_spectrum"] = Spectrum1D(
                            flux=flux_obs, spectral_axis=wavelength
                        )
                        spectra["residual_spectrum"] = Spectrum1D(
                            flux=residual_flux, spectral_axis=wavelength
                        )
                    except IndexError as e:
                        print(f"Error creating spectrum for {key}: {e}")
                    except TypeError as e:
                        print(f"Error creating spectrum for {key}: {e}")
                else:
                    print(
                        (
                            f"Data item {key} is a QTable"
                            " but does not have two 2 or 3 columns"
                        )
                    )
            else:
                print(f"Data item {key} is not a QTable")

        return spectra

    def make_plots(self):
        """Generate plots from spectra created with make_spectrum."""
        """
            spectra = self.make_spectrum()
            for key, spectrum in spectra.items():
               make_plot_base(spectrum.spectral_axis, spectrum.flux, key)
            """
        pass
