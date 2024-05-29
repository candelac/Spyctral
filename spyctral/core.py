# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# IMPORTS
# =============================================================================

from astropy.table import QTable
from astropy.units import Quantity

import attrs

import pandas as pd

from specutils import Spectrum1D

from .utils.bunch import Bunch

# from plot_utils import make_plot_base

# =============================================================================
# Useful functions
# =============================================================================

def header_to_dataframe(header):
    """Convert the header into a ``pandas.DataFrame``."""
    keys = list(header.keys())
    values = list(header.values())
    df = pd.DataFrame(values, index=keys)
    return df

def make_spectrum(obj):
    """Create spectra from data"""
    spectra = {}
    for key, value in obj.data.items():
        if isinstance(value, QTable):
            if len(value.columns) == 2:
                try:
                    wavelength = value.columns[0]
                    flux = value.columns[1]
                    spectra[key] = Spectrum1D(flux=flux, spectral_axis=wavelength)
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
                    spectra["synthetic_spectrum"] = Spectrum1D(flux=flux_syn, spectral_axis=wavelength)
                    spectra["observed_spectrum"] = Spectrum1D(flux=flux_obs, spectral_axis=wavelength)
                    spectra["residual_spectrum"] = Spectrum1D(flux=residual_flux, spectral_axis=wavelength)
                except IndexError as e:
                    print(f"Error creating spectrum for {key}: {e}")
                except TypeError as e:
                    print(f"Error creating spectrum for {key}: {e}")
            else:
                print(f"Data item {key} is a QTable but does not have two or three columns")
        else:
            print(f"Data item {key} is not a QTable")
    return spectra

# =============================================================================
# CLASSES 
# =============================================================================

@attrs.define
class SpectralSummary:
    """This object encapsulates all the data getted from inputfile.

    Attributes
    ----------
    header : dict-like 
        header info from inputfile
    data : dict-like
        spectra information in Qtables
    """

    header: dict = attrs.field(converter=lambda v: Bunch("header_items:", v))
    data: dict = attrs.field(converter=lambda v: Bunch("data_items:", v))

    @property
    def header_info_df(self) -> pd.DataFrame:
        return header_to_dataframe(self.header)

    @property
    def spectra(self) -> dict:
        return make_spectrum(self)

    def __getitem__(self, k):
        # Permite el acceso a los atributos de la instancia como si fuera un diccionario.
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError(k)

    def __len__(self):
        # Devuelve la cantidad de atributos definidos en la clase SpectralSummary.
        return len(attrs.fields(SpectralSummary))

    def __repr__(self):
        # Devuelve una representación en cadena de la instancia.
        return f"SpectralSummary(header={str(self.header)}, data={str(self.data)})"

    def make_plots(self):
        """Generate plots from spectra created with make_spectrum."""
        # Esta función está comentada y no se ejecuta.
        """
        spectra = self.make_spectrum()
        for key, spectrum in spectra.items():
            make_plot_base(spectrum.spectral_axis, spectrum.flux, key)
        """
        pass
