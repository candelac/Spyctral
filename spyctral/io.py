#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import re

import dateutil.parser

import numpy as np

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
    spectra_names = tuple(name for _, name in sorted(spectra_names.items()))

    header = {
        "fisa_version": fisa_version,
        "date_time": datetime,
        "reddening": reddening,
        "adopted_template": adopted_template,
        "normalization_point": normalization_point,
        "spectra_names": spectra_names,
    }

    return header


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
    header_lines, spectra_lines = [], []
    current_spectrum = []
    with open(path_or_buffer, "r") as fp:
        for line in fp:
            if line.startswith(" #"):
                header_lines.append(line.strip())
            elif line.strip():
                lamb, flux = map(float, line.split())
                current_spectrum.append([lamb, flux])
            elif current_spectrum and not line.strip():
                spectra_lines.append(np.array(current_spectrum, dtype=float))
                current_spectrum = []

    if current_spectrum:
        spectra_lines.append(np.array(current_spectrum, dtype=float))
        del current_spectrum

    header = _process_header(header_lines)

    return core.SpectralSummary(None, header=header)
