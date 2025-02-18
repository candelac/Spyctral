# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# File process
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================


import re

import astropy.units as u
from astropy.table import QTable

import dateutil.parser

from specutils import Spectrum1D

from spyctral.core import core


# =============================================================================
# FUNCTIONS
# =============================================================================

# FISA_RX_VERSION
# Extracts the FISA version from the file header.

# Examples
# --------
# Captures a line like:
#    SPECTRUM ANALYZED WITH FISA v. 0.92

FISA_RX_VERSION = re.compile(
    r"SPECTRUM ANALYZED WITH FISA v\.\s+(?P<value>[\d.][^\n]+)"
)



# FISA_RX_DATE_AND_TIME
# Extracts the date and time of the analysis.

# Examples
# --------
#Captures a line like:
#    Date 07/09/2022; time 10:11:03

FISA_RX_DATE_AND_TIME = re.compile(
    r"Date (?P<date>\d{2}/\d{2}/\d{4}); time (?P<time>\d{2}:\d{2}:\d{2})"
)



# FISA_RX_REDDENING
# Extracts the reddening value from the file header.

# Examples
# --------
# Captures a line like:
#    Reddening: 0.14

FISA_RX_REDDENING = re.compile(r"Reddening:\s+(?P<value>[\d.][^\n]+)")


# FISA_RX_TEMPLATE
# Extracts the path of the adopted template from the file header.

# Examples
# --------
# Captures a line like:
#    Adopted Template: /path/to/template.dat

FISA_RX_TEMPLATE = re.compile(r"Adopted Templated:\s*(?P<ruta>[\S]+)")


# FISA_RX_NORMALIZATION_POINT
# Extracts the normalization point from the file header.

# Examples
# --------
# Captures a line like:
#     Normalization Point: 5535.87988

FISA_RX_NORMALIZATION_POINT = re.compile(
    r"Normalization Point:\s+(?P<value>[\d.][^\n]+)"
)


# FISA_RX_SPECTRA_NAMES
# Extracts the spectrum names and their indices from the file header.

# Examples
# --------
# Captures a line like:
#    Index 0 = Unreddened spectrum

FISA_RX_SPECTRA_NAMES = re.compile(r"Index (?P<index>\d) = (?P<value>[^\n]+)")


# =============================================================================
# DEFAULT MAPS
# =============================================================================

"""
FISA_DEFAULT_AGE_MAP
Defines the age values (in years) for each spectral template.

Examples
--------
"G1": 13e9  # 13 billion years
"ya_lmc": 3e6  # 3 million years
"""
FISA_DEFAULT_AGE_MAP = {
    "G1": 13e9,
    "G2": 13e9,
    "G3": 13e9,
    "G4": 13e9,
    "G5": 13e9,
    "ya_lmc": 3e6,
    "yba_be": 4e6,
    "Ya1": 2e6,
}

"""
FISA_DEFAULT_ERROR_AGE_MAP
Defines the error values in age (in years) for each spectral template.

Examples
--------
"G1": 1e9  # Error of 1 billion years
"""
FISA_DEFAULT_ERROR_AGE_MAP = {
    "G1": 1e9,
    "G2": 1e9,
    "G3": 1e9,
    "G4": 1e9,
    "G5": 1e9,
    "ya_lmc": 1e6,
    "yba_be": 1e6,
    "Ya1": 1e6,
}

"""
FISA_DEFAULT_Z_MAP
Defines the metallicity values for each spectral template.

Examples
--------
"G1": 1.00  # Solar metallicity
"G5": -1.9  # Low metallicity
"""
FISA_DEFAULT_Z_MAP = {
    "G1": 0.19,
    "G2": 0.00756403,
    "G3": 0.0019,
    "G4": 0.00060083,
    "G5": 0.00023919,
    "ya_lmc": 0.04997509,
    "yba_be": 0.04997509,
    "Ya1": 0.19,
}


def _process_header(lines):
    """
    Function that processes the header lines of a FISA file and extracts
    key information, such as the FISA version, date, reddening value, adopted
    template, normalization point, and spectrum names.

    Parameters
    ----------
    lines : list of str
        List of strings representing the header lines of the FISA file.

    Returns
    -------
    dict
        A dictionary containing the following information:

            - **'fisa_version'** (*str*): Version of FISA used.
            - **'date_time'** (*datetime*): Date and time of the analysis.
            - **'reddening'** (*float*): Reddening value.
            - **'adopted_template'** (*str*): Path of the adopted template.
            - **'normalization_point'** (*float*): Normalization point.
            - **'spectra_names'** (*tuple of str*): Spectrum names indexed by
                position.
    """
    src = "\n".join(lines)

    fisa_version = FISA_RX_VERSION.findall(src)[0]

    date, time = FISA_RX_DATE_AND_TIME.findall(src)[0]
    datetime = dateutil.parser.parse(f"{date} {time}")

    reddening = float(FISA_RX_REDDENING.findall(src)[0])
    adopted_template = FISA_RX_TEMPLATE.findall(src)[0]
    normalization_point = float(FISA_RX_NORMALIZATION_POINT.findall(src)[0])

    spectra_names = {}
    for match in FISA_RX_SPECTRA_NAMES.finditer(src):
        idx = int(match.group("index"))
        name = match.group("value")
        spectra_names[idx] = name
    spectra_names = tuple(
        name.replace(" ", "_") for _, name in sorted(spectra_names.items())
    )

    header = {
        "fisa_version": fisa_version,
        "date_time": datetime,
        "reddening": reddening,
        "adopted_template": adopted_template,
        "normalization_point": normalization_point,
        "spectra_names": spectra_names,
    }

    return header


def _fisa_spectra_names(spectra, table_names):
    """
    Renames the spectral tables by associating each spectrum with its
    corresponding name, based on a list of table names.

    Parameters
    ----------
    spectra : list
        List of spectral tables ('QTable' objects) that have been processed.
    table_names : tuple of str
        Tuple of strings representing the names associated with each spectrum.

    Returns
    -------
    dict
        A dictionary where the keys are table names and the values are the
        corresponding spectral tables.
    """
    renamed_spectra = {
        table_name: table for table_name, table in zip(table_names, spectra)
    }
    return renamed_spectra


def _process_blocks(spectra_blocks, tab_names):
    """
    Processes spectral data blocks extracted from a FISA file and converts them
    into structured tables with columns for wavelength and normalized flux.

    Parameters
    ----------
    spectra_blocks : list of list of str
        List of spectral blocks, where each block contains lines of
        text-formatted data.
    tab_names : tuple of str
        Tuple of strings representing the names associated with each spectrum.

    Returns
    -------
    dict
        A dictionary where keys are table names (tab_names) and values are
        spectral tables ('QTable') with the following columns:

            - **'Wavelength'** (*Quantity*): Wavelength values in Angstroms).
            - **'Normalizated_flux'** (*float*): Normalized flux values.
    """

    spectra = []

    for block in spectra_blocks:
        block_data = []
        column_names = [
            "Wavelength",
            "Normalizated_flux",
        ]
        for line in block:
            elements = list(map(float, line.strip().split()))
            block_data.append(elements)

        if column_names and block_data:
            table = QTable(rows=block_data, names=column_names)
            table["Wavelength"].unit = u.Angstrom
            spectra.append(table)

    spectra_tables = _fisa_spectra_names(spectra, tab_names)

    return spectra_tables


def _get_str_template(header):
    """
    Extracts the filename of the adopted template from the header.

    Parameters
    ----------
    header : dict
        Dictionary containing the header information of the FISA file,
        including the full path of the adopted template in the
        'adopted_template' key.

    Returns
    -------
    str
        The filename of the adopted template, including its extension.
    """
    template = header["adopted_template"]
    str_template = template.split("/")[-1]

    return str_template


def _get_name_template(header):
    """
    Retrieves the base name of the adopted template from the header of the
    FISA file. The base name is the filename without the extension.

    Parameters
    ----------
    header : dict
        Dictionary containing the header information of the FISA file,
        including the full path of the adopted template in the
        'adopted_template' key.

    Returns
    -------
    str
        The base name of the adopted template, without its extension.
    """
    template = header["adopted_template"]
    name_template = (template.split("/")[-1]).split(".")[0]

    return name_template


def _get_reddening(header, rv):
    """
    Calculates the reddening value and its equivalent extinction magnitude
    (A_v), based on the value provided in the FISA file header and the
    reddening parameter (R_v).

    Parameters
    ----------
    header : dict
        Dictionary containing the header information of the FISA file.
    rv : float
        Reddening parameter (R_v), typically 3.1 for the interstellar medium.

    Returns
    -------
    tuple of float
        A tuple containing:

        - **'reddening_value'** (*float*): Reddening value extracted from the
            header.
        - **'av_value'** (*float*): Extinction magnitude (A_v) calculated as
          'reddening_value * R_v'.
    """

    reddening_value = header["reddening"]
    av_value = reddening_value * rv

    return reddening_value, av_value


def _get_spectra(data):
    """
    Converts the processed spectral data into a dictionary of 'Spectrum1D'
    objects, representing spectra with wavelength and flux.

    Parameters
    ----------
    data : dict
        Dictionary where keys are spectrum names and values are spectral tables
        ('QTable') with columns for wavelength and normalized flux.

    Returns
    -------
    dict
        A dictionary where the keys are spectrum names and values are
        'Spectrum1D' objects containing the flux and wavelength data.
    """

    spectra = {}
    for key, value in data.items():
        wavelength = value[value.colnames[0]]
        flux = value[value.colnames[1]]
        spectra[key] = Spectrum1D(
            flux=flux * u.dimensionless_unscaled, spectral_axis=wavelength
        )

    return spectra


def read_fisa(
    path_or_buffer,
    *,
    age_map=None,
    error_age_map=None,
    rv=3.1,
    z_map=None,
    object_name="object_1",
):
    """
    Reads a FISA file and extracts the spectral data, including the header and
    data columns.

    Parameters
    ----------
    path_or_buffer : str
        Path and name of the FISA file to read.

    age_map : dict or None, optional
        Mapping dictionary for age values.
        If None, defaults to FISA_DEFAULT_AGE_MAP.
        (default: None)

    rv : float, optional
        Reddening value to use for calculations.
        (default: 3.1)

    z_map : dict or None, optional
        Mapping dictionary for metallicity values.
        If None, defaults to FISA_DEFAULT_Z_MAP.
        (default: None)

    Returns
    -------
    SpectralSummary
        An object containing encapsulated data extracted from the FISA file.
    dict
        A dictionary with the following keys:

        - **'header'** (*list*): Lines of the file's header.
        - **'data'** (*ndarray*): Spectral data in NumPy array format.
        - **'reddening'** (*float*): Reddening value extracted from the header.
        - **'template'** (*str*): Path of the template used, extracted from the
            header.
        - *'norm_point'** (*float*): Normalization point extracted from the
            header.

    Notes
    -----
    Function that processes a FISA file, extracting header information and
    spectral blocks. It computes age, reddening, AV value, normalization point,
    and metallicity values based on the provided or default mappings.
    """

    age_map = FISA_DEFAULT_AGE_MAP if age_map is None else age_map
    error_age_map = (
        FISA_DEFAULT_ERROR_AGE_MAP if error_age_map is None else error_age_map
    )
    z_map = FISA_DEFAULT_Z_MAP if z_map is None else z_map

    obj_name = object_name

    header_lines, spectra_blocks = [], []
    current_spectrum = []

    with open(path_or_buffer, "r") as fp:
        for line in fp:
            if line.startswith(" #"):
                header_lines.append(line.strip())
            elif line.strip():
                current_spectrum.append(line)
            elif current_spectrum and not line.strip():
                spectra_blocks.append(current_spectrum)
                current_spectrum = []

    if current_spectrum:
        spectra_blocks.append(current_spectrum)

    header = _process_header(header_lines)
    data = _process_blocks(spectra_blocks, header.get("spectra_names"))

    str_template = _get_str_template(header)
    name_template = _get_name_template(header)

    try:
        age = age_map[name_template]
    except KeyError:
        raise ValueError(
            f"Missing age mapping for template '{name_template}' "
            "in age_map."
        )

    err_age = error_age_map[name_template]
    reddening_value, av_value = _get_reddening(header, rv)
    normalization_point = header["normalization_point"]

    try:
        z_value = z_map[name_template]
    except KeyError:
        raise ValueError(
            f"Missing metallicity mapping for template '{name_template}' "
            "in z_map."
        )

    spectra = _get_spectra(data)

    extra_info = {
        "str_template": str_template,
        "name_template": name_template,
        "age_map": age_map,
        "error_age_map": error_age_map,
        "z_map": z_map,
    }

    return core.SpectralSummary(
        obj_name=obj_name,
        header=header,
        data=data,
        age=age,
        err_age=err_age,
        reddening=reddening_value,
        av_value=av_value,
        normalization_point=normalization_point,
        z_value=z_value,
        spectra=spectra,
        extra_info=extra_info,
    )
