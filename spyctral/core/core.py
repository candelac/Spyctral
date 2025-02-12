# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# IMPORTS
# =============================================================================

import attrs

import numpy as np

import pandas as pd

from ..utils.bunch import Bunch


# =============================================================================
# CONSTANTS
# =============================================================================

#: Z sun (cite)
Z_SUN = 0.019


# =============================================================================
# USEFUL FUNCTIONS
# =============================================================================


def _header_to_dataframe(header):
    """
    Converts a given header (in dictionary form) into a pandas DataFrame.

    Parameters
    ----------
    header : dict
        Dictionary containing the header keys and values.

    Returns
    -------
    pandas.DataFrame
        DataFrame with header keys as the index and values in a column named
        "value".
    """
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
    """
    Class that encapsulates all the data obtained from an input file.

    Attributes
    ----------
    obj_name : str
        Object name.
    header : dict
        Header information from the input file.
    data : dict
        Spectra information in QTable format.
    age : float
        Object's age.
    err_age : float
        Error associated with the age.
    reddening : float
        Value of reddening
    av_value : float
        Extinction value.
    normalization_point : float
        Value of the normalization point.
    z_value : float
        Metallicity value.
    spectra : dict
        Set of spectra extracted from the input file.
    extra_info : dict
        Additional information.
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
        """
        Converts the information stored in the 'header' attribute into a pandas
        DataFrame.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the header information, where the header
            keys are the index and the values are stored in a column named
            "value".
        """
        return _header_to_dataframe(self.header)

    def get_spectrum(self, name: str):
        """
        Retrieves a specific spectrum from the 'spectra' attribute.

        Parameters
        ----------
        name : str
            The Name of the spectrum to retrieve.

        Returns
        -------
        Spectrum
            The spectrum corresponding to the specified name.
        """
        return self.spectra[name]

    def __getitem__(self, k: str):
        """
        Allows access to the class attributes using dictionary-like syntax.

        Parameters
        ----------
        k : str
            The name of the attribute to retrieve.

        Returns
        -------
        Any
            The value of the requested attribute.

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
        """
        Returns the number of attributes defined in the class.

        Returns
        -------
        int
            The total number of attributes defined in the class.
        """

        return len(attrs.fields(SpectralSummary))

    def __repr__(self) -> str:
        """
        Returns a string representation of the class instance, including a
        summary of the main attributes: header, data, spectra, and
        additional information.

        Returns
        -------
        str
            A string representation of the instance.
        """
        header_keys = ", ".join(self.header.keys())
        data_keys = ", ".join(self.data.keys())
        spectra_keys = ", ".join(self.spectra.keys())
        extra_info_keys = ", ".join(self.extra_info.keys())

        return (
            f"<SpectralSummary(\n"
            f"  header={{{header_keys}}},\n"
            f"  data={{{data_keys}}},\n"
            "  age, reddening, av_value, normalization_point, z_value,\n"
            f"  spectra={{{spectra_keys}}},\n"
            f"  extra_info={{{extra_info_keys}}})>"
        )

    @property
    def feh_ratio(self):
        """
        Calculates the metallicity ratio [Fe/H] using the instance's Z value
        and the solar constant ('Z_SUN').

        Returns
        -------
        float
            Metallicity ratio [Fe/H].
        """
        feh_ratio = np.log10(self.z_value / Z_SUN)

        return feh_ratio

    @property
    def plot(self):
        """
        Generates a 'SpectralPlotter' object for plotting the spectra stored
        in the instance.
        Uses the 'SpectralPlotter' class to handle plotting functionalities.

        Returns
        -------
        SpectralPlotter
            Object that enables generating plots of the spectra.
        """
        from .plot import SpectralPlotter

        return SpectralPlotter(self)

    @property
    def get_all_properties(self) -> pd.DataFrame:
        """
        Creates a DataFrame containing all relevant parameters of the instance.
        Numerical values are formatted to display in scientific notation where
        necessary.

        Returns
        -------
        pandas.DataFrame
            A DataFrame with two columns: "Property" and "Value".
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
