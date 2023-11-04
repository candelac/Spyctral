#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import re

import astropy.units as u
from astropy.table import QTable

import dateutil.parser

from . import core

FISA_RX_VERSION = re.compile(
    r"SPECTRUM ANALYZED WITH FISA v\.\s+(?P<value>[\d.][^\n]+)"
)

FISA_RX_DATE_AND_TIME = re.compile(
    r"Date (?P<date>\d{2}/\d{2}/\d{4}); time (?P<time>\d{2}:\d{2}:\d{2})"
)

FISA_RX_REDDENING = re.compile(r"Reddening:\s+(?P<value>[\d.][^\n]+)")

FISA_RX_TEMPLATE = re.compile(r"Adopted Templated:\s*(?P<ruta>[\S]+)")

FISA_RX_NORMALIZATION_POINT = re.compile(
    r"Normalization Point:\s+(?P<value>[\d.][^\n]+)"
)

FISA_RX_SPECTRA_NAMES = re.compile(r"Index (?P<index>\d) = (?P<value>[^\n]+)")


def _process_header(lines):
    """
    This function processes header lines.
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
    renamed_spectra = {
        table_name: table for table_name, table in zip(table_names, spectra)
    }
    return renamed_spectra


def _process_blocks(spectra_blocks, tab_names):
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


def read_fisa(path_or_buffer):
    """
    This function reads FISA file.

    Parameters
    ----------
    filename: "str"
        Name of file

    Return
    ----------
    out: SpectralSummary

    """
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
        del current_spectrum

    header = _process_header(header_lines)

    spectra = _process_blocks(spectra_blocks, header.get("spectra_names"))

    return core.SpectralSummary(header=header, data=spectra)
