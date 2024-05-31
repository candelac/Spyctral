# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# IMPORTS
# =============================================================================

import astropy.units as u
from astropy.table import QTable

import attrs

import numpy as np

import pandas as pd

from specutils import Spectrum1D

from .utils.bunch import Bunch

# from plot_utils import make_plot_base

# =============================================================================
# Useful functions
# =============================================================================


def _header_to_dataframe(header):
    """Convert the header into a ``pandas.DataFrame``."""
    keys = list(header.keys())
    values = list(header.values())
    df = pd.DataFrame(values, index=keys)
    return df


def _make_spectrum1d_from_qtable(qtable):
    """
    Creates a Spectrum1D object from a QTable.

    Parameters:
    - qtable (QTable): The table containing the data.

    Returns:
    - dict: A dictionary with the Spectrum1D objects created
            from the QTable data.
            The keys are 'synthetic_spectrum', 'observed_spectrum',
            and 'residual_spectrum'.
    """

    # Verify that the required columns are present in the QTable
    required_columns = ["l_obs", "f_obs", "f_syn", "weights"]
    for col in required_columns:
        if col not in qtable.colnames:
            raise ValueError(
                f"The column '{col}' is not present in the QTable."
            )

    # Extract the necessary columns
    wavelength = qtable["l_obs"]
    flux_obs = qtable["f_obs"].data  # Extract data without units
    flux_syn = qtable["f_syn"].data  # Extract data without units
    weights = qtable["weights"].data

    # Calculate the residual flux
    residual_flux = (flux_obs - flux_syn) / flux_obs

    # Create the Spectrum1D objects
    spectra = {
        "synthetic_spectrum": Spectrum1D(
            flux=flux_syn * u.dimensionless_unscaled, spectral_axis=wavelength
        ),
        "observed_spectrum": Spectrum1D(
            flux=flux_obs * u.dimensionless_unscaled, spectral_axis=wavelength
        ),
        "residual_spectrum": Spectrum1D(
            flux=residual_flux * u.dimensionless_unscaled,
            spectral_axis=wavelength,
        ),
    }

    return spectra


def make_spectrum(obj):
    """Crear espectros a partir de datos"""
    spectra = {}
    for key, value in obj.data.items():
        if isinstance(value, QTable):
            if len(value.columns) == 2:
                try:
                    # Extraer datos de las columnas
                    wavelength = value[value.colnames[0]]
                    flux = value[value.colnames[1]]

                    # Validar que los datos sean tipos numéricos
                    if np.issubdtype(
                        wavelength.dtype, np.number
                    ) and np.issubdtype(flux.dtype, np.number):
                        spectra[key] = Spectrum1D(
                            flux=flux * u.dimensionless_unscaled,
                            spectral_axis=wavelength,
                        )
                    else:
                        raise TypeError(
                            f"Error al crear el espectro para {key}:"
                            "la longitud de onda y el flujo deben ser"
                            " tipos numéricos"
                        )
                except (IndexError, TypeError) as e:
                    raise ValueError(
                        f"Error al crear el espectro para {key}: {e}"
                    )
            elif len(value.columns) == 4 and key == 'synthetic_spectrum':
                try:
                    print("Value:", value)
                    spectra.update(_make_spectrum1d_from_qtable(value))
                    print(spectra)
                except (IndexError, TypeError) as e:
                    raise ValueError(
                        f"Error al crear el espectro para {key}: {e}"
                    )
            else:
                None
    return spectra


"""
def make_spectrum(obj):
    spectra = {}
    for key, value in obj.data.items():
        if isinstance(value, QTable):
            if len(value.columns) == 2:
                try:
                    wavelength = value.columns[0]
                    flux = value.columns[1]

                    # Verificar que los datos sean tipos numéricos válidos
                    if isinstance(
                        wavelength, (int, float, np.number)
                    ) and isinstance(flux, (int, float, np.number)):
                        spectra[key] = Spectrum1D(
                            flux=flux, spectral_axis=wavelength
                        )
                    else:
                        raise TypeError(
                            f"Error creating spectrum for {key}:"
                            " wavelength and flux must be numeric types"
                        )
                except (IndexError, TypeError) as e:
                    raise ValueError(f"Error creating spectrum for {key}: {e}")
            elif key == "synthetic_spectrum" and len(value.columns) == 4:
                try:
                    wavelength = value.columns[0]
                    flux_obs = value.columns[1]
                    flux_syn = value.columns[2]

                    # Verificar que los datos sean tipos numéricos válidos
                    if (
                        isinstance(wavelength, (int, float, np.number))
                        and isinstance(flux_obs, (int, float, np.number))
                        and isinstance(flux_syn, (int, float, np.number))
                    ):
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
                    else:
                        raise TypeError(
                            f"Error creating spectrum for {key}:"
                            " wavelength, flux_obs, and flux_syn"
                            " must be numeric types"
                        )
                except (IndexError, TypeError) as e:
                    raise ValueError(f"Error creating spectrum for {key}: {e}")
            else:
                raise ValueError(
                    f"Data item {key} is a QTable but "
                    "does not have two or three columns"
                )
        else:
            raise TypeError(f"Data item {key} is not a QTable")
    return spectra
"""

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
        return _header_to_dataframe(self.header)

    @property
    def spectra(self) -> dict:
        return make_spectrum(self)

    def get_spectrum(self, name):
        """Get the spectrum by name."""
        try:
            return self.spectra[name]
        except KeyError:
            print(f"Spectrum '{name}' not found.")
            return None

    def __getitem__(self, k):
        # Permite el acceso a los atributos de la
        # instancia como si fuera un diccionario.
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError(k)

    def __len__(self):
        # Devuelve la cantidad de atributos
        # definidos en la clase SpectralSummary.
        return len(attrs.fields(SpectralSummary))

    def __repr__(self):
        # Devuelve una representación en
        # cadena de la instancia.
        return (
            f"SpectralSummary(header={str(self.header)}, "
            f"data={str(self.data)})"
        )

    def make_plots(self):
        """Generate plots from spectra created with make_spectrum."""
        # Esta función está comentada y no se ejecuta.
        """
        spectra = self.make_spectrum()
        for key, spectrum in spectra.items():
            make_plot_base(spectrum.spectral_axis, spectrum.flux, key)
        """
        pass
