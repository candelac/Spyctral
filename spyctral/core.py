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
    # weights = qtable["weights"].data

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
            elif len(value.columns) == 4 and key == "synthetic_spectrum":
                try:
                    spectra.update(_make_spectrum1d_from_qtable(value))

                except (IndexError, TypeError) as e:
                    raise ValueError(
                        f"Error al crear el espectro para {key}: {e}"
                    )
            else:
                None
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
        Header info from inputfile.
    data : dict-like
        Spectra information in Qtables.
    age : float
        Age information.
    reddening : float
        Reddening information.
    av_value : float
        Av value.
    normalization_point : float
        Normalization point value.
    z_value : float
        Metallicity value.
    extra_info : dict-like
        Additional info.
    """

    header: dict = attrs.field(converter=lambda v: Bunch("header", v))
    data: dict = attrs.field(converter=lambda v: Bunch("data", v))
    age: float = attrs.field(converter=float)
    reddening: float = attrs.field(converter=float)
    av_value: float = attrs.field(converter=float)
    normalization_point: float = attrs.field(converter=float)
    z_value: float = attrs.field(converter=float)
    extra_info: dict = attrs.field(converter=lambda v: Bunch("extra", v))

    @property
    def header_info_df(self) -> pd.DataFrame:
        """Convert header info to a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame containing header information.
        """
        return _header_to_dataframe(self.header)

    @property
    def spectra(self) -> dict:
        """Generate spectra from data.

        Returns
        -------
        dict
            Dictionary containing the spectra information.
        """
        return make_spectrum(self)

    def get_spectrum(self, name: str):
        """Get the spectrum by name.

        Parameters
        ----------
        name : str
            Name of the spectrum.

        Returns
        -------
        Spectrum
            The spectrum corresponding to the given name.
        """
        return self.spectra[name]

    def __getitem__(self, k: str):
        """Allow attribute access using dictionary-like syntax.

        Parameters
        ----------
        k : str
            Attribute name.

        Returns
        -------
        Any
            Value of the attribute.

        Raises
        ------
        KeyError
            If the attribute does not exist.
        """
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError(k)

    def __len__(self) -> int:
        """Return the number of attributes defined in the class.

        Returns
        -------
        int
            Number of attributes.
        """
        return len(attrs.fields(SpectralSummary))

    def __repr__(self) -> str:
        """Return a string representation of the instance.

        Returns
        -------
        str
            String representation.
        """
        return (
            f"SpectralSummary(header={str(self.header)}, "
            f"data={str(self.data)})"
        )

    def get_metallicity(self) -> dict:
        """Calculate metallicity value from Z value.

        Returns
        -------
        dict
            Dictionary with z_value and [Fe/H] ratio.
        """
        z_sun = 0.019
        feh_ratio = np.log10(self.z_value / z_sun)

        metallicity_info = {"Z_value": self.z_value, "[Fe/H]": feh_ratio}

        return metallicity_info

    def make_plots(self):
        """Generate plots from spectra created with make_spectrum.

        This function is currently commented out and does not execute.
        """
        # Esta función está comentada y no se ejecuta.
        """
        spectra = self.spectra
        for key, spectrum in spectra.items():
            make_plot_base(spectrum.spectral_axis, spectrum.flux, key)
        """
        pass
