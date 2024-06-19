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

# import pandas as pd

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

def _get_age(tables_dict, x_j_gt, decimals):
    
    df = starlight.tabla_synthesis_results
    df = df[df["x_j(%)"] > x_j_gt]

    age = int(
        10
        ** (
            ((df["x_j(%)"] * np.log10(df["age_j(yr)"]))).sum()
            / df["x_j(%)"].sum()
        )
    )
    age = np.log10(age)
    age = round(age, decimals)

    return age

def read_starlight(path, *, x_j_gt=5, decimals=2):
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

    # return header_info, tables_dict
    age= _get_age(tables_dict, x_j_gt, decimals)
    extra = {'x_j_gt':x_j_gt, 'decimals': decimals}
    return core.SpectralSummary(age=age, extra=extra, header=header_info, data=tables_dict)
