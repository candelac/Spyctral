# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import re

import astropy.units as u
from astropy.table import QTable

import dateutil.parser

import numpy as np

import pandas as pd

from spyctral import core


SL_GET_HEADER = re.compile(r"\[")
SL_GET_TITLE_VALUE = re.compile(r"\[")
SL_REPLACE_AND = re.compile(r"&")
SL_GET_MULTIPLE_VALUES = re.compile(r",")
SL_GET_DATE = re.compile(r"\b\d{2}/[a-zA-Z]{3}/\d{4}\b")
PATRON = re.compile(r"#(.*?)(?:(?=\n)|$)")


def _proces_header(header_ln):
    """Recives as input a list with the lines of the header and returns a
    dictionary with the parameters and values"""

    head_dict = {}
    for sl in header_ln:
        if re.findall(SL_GET_DATE, sl):
            head_dict["Date"] = dateutil.parser.parse(
                re.findall(SL_GET_DATE, sl)[0]
            )
            head_dict["user"] = sl.split("[")[1].split("-")[0].strip()

        sl = re.sub(
            r"\s{2,}", " ", sl.replace("&", ",").replace("]\n", "")
        ).replace("/", "_")

        # Handles string with multiple values on the same line.
        # They are idenfied by havin a ','
        if re.findall(SL_GET_MULTIPLE_VALUES, sl):
            starline_values = (
                sl.split("[")[0].strip().split(" ")
            )  # keeps the values
            starline_var = sl.split("[")[1].split(
                ","
            )  # keeps the names of the variables

            for pos, val in enumerate(starline_values):
                if bool(
                    re.search(r"[0-9]", val)
                ):  # filters for numeric values
                    head_dict[starline_var[pos].strip().split(" ")[0]] = float(
                        val
                    )
                else:
                    head_dict[starline_var[pos].strip().split(" ")[0]] = val

        # Handles string with S/N titles that repeats
        # overlaps if not handled.
        elif re.findall(r"\[S_N", sl):
            starline_list = sl.split("[")
            head_dict[
                starline_list[1].replace(" ", "_").replace(".", "").strip()
            ] = float(starline_list[0])

        # saves all the other values
        # that not contain any special exception
        else:
            starline_list = sl.replace("-", "_").replace("#", "").split("[")
            if bool(re.search(r"[0-9]", starline_list[0])) and not bool(
                re.search(r"[a-z]", starline_list[0])
            ):  # filters for numeric values
                head_dict[starline_list[1].split(" ")[0]] = float(
                    starline_list[0].replace("_", "-").strip()
                )
            else:
                head_dict[starline_list[1].split(" ")[0]] = starline_list[
                    0
                ].strip()

    return head_dict


def _proces_tables(block_lines):
    """Recives a list that contains the lines of the tables and
    return a dictionary with 4 tables as values"""
    block_titles = []
    blocks = []
    tab = []
    for sl in block_lines:
        # This part procces the tables
        if (
            re.search(SL_GET_TITLE_VALUE, sl) is None
            and re.match("##", sl) is None
        ):
            # Filters the titles of the tables
            if re.search(r"# ", sl):
                block_titles.append(sl)
            # Filters the empty spaces
            elif len(sl) > 1:
                # print(sl)
                sl = re.sub(r"\s{2,}", " ", sl.strip())
                tab.append(sl.split(" "))

            # Generates a block for each empty line that founds
            # and if the block is larger it appends it
            else:
                if len(tab) > 1:
                    blocks.append(tab)
                    tab = []
    blocks.append(tab)
    tab = []
    first_title = (
        re.sub(r"\s{2,}", " ", block_titles[0][1:])
        .replace(".", "")
        .replace("?", "")
        .strip()
    )

    # Verificar que los elementos sean números
    for i, row in enumerate(blocks[4]):
        converted_row = []
        for item in row:
            try:
                # Intentar convertir el elemento en un número
                converted_item = float(item)
            except ValueError:
                # Si no se puede convertir a número, levantar una excepción
                raise ValueError(
                    f"Element at position ({i})"
                    " in 'synthetic_spectrum' table cannot "
                    "  be converted to a number."
                )
            converted_row.append(converted_item)
        blocks[4][i] = converted_row

    # Crear la tabla synthetic_spectrum con unidades
    synthetic_spectrum_table = QTable(
        rows=blocks[4], names=["l_obs", "f_obs", "f_syn", "weights"]
    )

    # Cambio: Agregar unidades a la columna 'l_obs'
    synthetic_spectrum_table["l_obs"].unit = u.AA

    spectra_dict = {
        # Cambio: Usar la tabla con unidades
        "synthetic_spectrum": synthetic_spectrum_table,
        "synthetic_results": QTable(
            rows=blocks[0], names=first_title.split(" ")
        ),
        "results_average_chains_xj": QTable(rows=blocks[1]),
        "results_average_chains_mj": QTable(rows=blocks[2]),
        "results_average_chains_Av_chi2_mass": QTable(
            rows=np.array(blocks[3]).T[1:],
            names=np.array(blocks[3]).T[0],
        ),
    }

    return spectra_dict


def _get_ssp_contributions(tables_dict, xj_percent):
    ssps_vector = tables_dict["synthetic_results"]
    ssps_vector = (
        ssps_vector.to_pandas()
    )  # Convertir QTable a DataFrame de Pandas

    # Convertir todas las columnas a números flotantes
    ssps_vector = ssps_vector.apply(pd.to_numeric, errors="coerce")

    ssps_vector = ssps_vector[ssps_vector["x_j(%)"] > xj_percent].reset_index(
        drop=True
    )
    ssps_vector["x_j(%)"] = (
        ssps_vector["x_j(%)"] * 100 / ssps_vector["x_j(%)"].sum()
    )

    return ssps_vector


def _get_age(ssps_vector, age_decimals):
    """
    This function get age from input file.
    """

    age = int(
        10
        ** (
            (
                (ssps_vector["x_j(%)"] * np.log10(ssps_vector["age_j(yr)"]))
            ).sum()
            / ssps_vector["x_j(%)"].sum()
        )
    )
    age = np.log10(age)
    age = round(age, age_decimals)

    return age


def _get_reddening(header_info, rv):
    """
    This function determinate reddening value from input file.
    """

    av_value = header_info["AV_min"]
    reddening_value = av_value / rv

    return reddening_value, av_value


def _get_metallicity(ssps_vector, z_decimals):
    """
    This function calculate metallicity value from input file.
    """

    z_value = (
        (ssps_vector["x_j(%)"] * ssps_vector["Z_j"])
    ).sum() / ssps_vector["x_j(%)"].sum()
    z_value = round(z_value, z_decimals)

    return z_value


def read_starlight(
    path, *, xj_percent=5, age_decimals=2, rv=3.1, z_decimals=3
):
    """Recives as input a path from the location of the starlight file and
    returns a two dicctionaries the first is the header information and the
    second is the tables information"""

    header_lines, block_lines = [], []
    with open(path) as starfile:
        for d, starline in enumerate(starfile):
            if re.findall(SL_GET_TITLE_VALUE, starline):
                header_lines.append(starline)
            else:
                block_lines.append(starline)

    header_info = _proces_header(header_lines)

    tables_dict = _proces_tables(block_lines)

    ssps_vector = _get_ssp_contributions(tables_dict, xj_percent)

    age = _get_age(ssps_vector, age_decimals)

    reddening_value, av_value = _get_reddening(header_info, rv)

    normalization_point = header_info["l_norm"]

    z_value = _get_metallicity(ssps_vector, z_decimals)

    extra = {
        "xj_percent": xj_percent,
        "age_decimals": age_decimals,
        "rv": rv,
        "z_decimals": z_decimals,
    }

    return core.SpectralSummary(
        header=header_info,
        data=tables_dict,
        age=age,
        reddening=reddening_value,
        av_value=av_value,
        normalization_point=normalization_point,
        z_value=z_value,
        ssps_vector=ssps_vector,
        extra=extra,
    )
