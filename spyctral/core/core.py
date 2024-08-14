# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# IMPORTS
# =============================================================================

# from .utils.bunch import Bunch
import attrs

import numpy as np

import pandas as pd

from ..utils.bunch import Bunch

# << << << < HEAD: spyctral/core.py


# from plot_utils import make_plot_base
# == == == =
# >>>>>> > main: spyctral/core/core.py

# =============================================================================
# CONSTANTS
# =============================================================================

#: Z sun (cite)
Z_SUN = 0.019


# =============================================================================
# USEFUL FUNCTIONS
# =============================================================================


def _header_to_dataframe(header):
    """Convert the header into a ``pandas.DataFrame``."""
    keys = list(header.keys())
    values = list(header.values())
    df = pd.DataFrame(values, index=keys)
    df.columns = ["value"]
    return df


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

    spectra: dict-like
        Spectrum set from data

    extra_info : dict-like
        Additional info.
    """

    obj_name: str = attrs.field(converter=str)
    header: dict = attrs.field(converter=lambda v: Bunch("header", v))
    data: dict = attrs.field(converter=lambda v: Bunch("data", v))
    age: float = attrs.field(converter=float)
    err_age: float = attrs.field(converter=float)
    reddening: float = attrs.field(converter=float)
    av_value: float = attrs.field(converter=float)
    normalization_point: float = attrs.field(converter=float)
    z_value: float = attrs.field(converter=float)
    spectra: dict = attrs.field(converter=lambda v: Bunch("spectra", v))
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

        header_keys = ", ".join(self.header.keys())
        data_keys = ", ".join(self.data.keys())
        spectra_keys = ", ".join(self.spectra.keys())
        extra_info_keys = ", ".join(self.extra_info.keys())

        return (
            f"SpectralSummary(\n"
            f"  header={{{header_keys}}},\n"
            f"  data={{{data_keys}}},\n"
            "  age, reddening, av_value, normalization_point, z_value,\n"
            f"  spectra={{{spectra_keys}}},\n"
            f"  extra_info={{{extra_info_keys}}})"
        )

    @property
    def feh_ratio(self):
        """Calculate metallicity value from Z value.

        Returns
        -------
        Class
            Metallicity with z_value and [Fe/H] ratio.
        """

        feh_ratio = np.log10(self.z_value / Z_SUN)

        return feh_ratio

    @property
    def plot(self):
        """Generate plots from spectra."""

        from .plot import SpectralPlotter

        return SpectralPlotter(self)

    @property
    def get_all_properties(self) -> pd.DataFrame:
        """Make a dataframe with all the parameter values.

        Returns
        -------
        pd.DataFrame
            DataFrame containing all the parameters values.
        """
        age = f"{self.age:.2e}"
        err_age = f"{self.err_age:.2e}"

        properties = {
            "object_name": self.obj_name,
            "age": age,
            "err_age": err_age,
            "reddening": self.reddening,
            "av_value": self.av_value,
            "z_value": self.z_value,
            "feh_ratio": self.feh_ratio,
            "normalization_point": self.normalization_point,
        }

        df = pd.DataFrame(
            list(properties.items()), columns=["Property", "Value"]
        )

        return df
