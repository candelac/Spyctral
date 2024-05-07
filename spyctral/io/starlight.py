# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import re
import pandas as pd
import numpy as np
from spyctral import core
from astropy.table import QTable


SL_GET_TITLE_VALUE = re.compile(r"\[")
SL_REPLACE_AND = re.compile(r"&")
SL_GET_MULTIPLE_VALUES = re.compile(r",")
SL_GET_DATE = re.compile(r"\b\d{2}/[a-zA-Z]{3}/\d{4}\b")
PATRON = re.compile(r"#(.*?)(?:(?=\n)|$)")


def read_star_light(path):
    with open(path) as starfile:
        summary_info = {}
        blocks = []
        tab = []
        block_titles = []
        for d, starline in enumerate(starfile):
            # Gets all the lines that contains '[' that means: 
            # all the summarized information.
            if re.findall(SL_GET_TITLE_VALUE, starline):
                # Cleaning of the string.
                if re.findall(SL_GET_DATE, starline):
                    summary_info["Date"] = re.findall(SL_GET_DATE, starline)[0]
                starline = re.sub(
                    r"\s{2,}",
                    " ",
                    starline.replace("&", ",").replace("]\n", ""),
                ).replace("/", "_")

                # Handles string with multiple values on the same line.
                if re.findall(SL_GET_MULTIPLE_VALUES, starline):
                    starline_list = starline.split("[")
                    try:
                        temp_dict = dict(
                            zip(
                                starline_list[1]
                                .strip()
                                .replace(" ", "")
                                .split(","),
                                float(starline_list[0].strip().split(" ")),
                            )
                        )
                    except:
                        temp_dict = dict(
                            zip(
                                starline_list[1]
                                .strip()
                                .replace(" ", "")
                                .split(","),
                                starline_list[0].strip().split(" "),
                            )
                        )
                    summary_info = {**summary_info, **temp_dict}

                # Handles string with SN titles that repeats and 
                # overlaps if not handled.
                elif re.findall(r"\[S_N", starline):
                    starline_list = starline.split("[")
                    try:
                        summary_info[
                            starline_list[1].split(" ")[0] + str(d)
                        ] = float(starline_list[0])
                    except:
                        summary_info[
                            starline_list[1].split(" ")[0] + str(d)
                        ] = starline_list[0]

                # Adds all the other normal values that do
                # not contain any exeption
                else:
                    starline_list = (
                        starline.replace("-", "_").replace("#", "").split("[")
                    )
                    try:
                        summary_info[starline_list[1].split(" ")[0]] = float(
                            starline_list[0].strip()
                        )
                    except:
                        summary_info[starline_list[1].split(" ")[0]] = (
                            starline_list[0].strip()
                        )

            # This part procces the tables
            if (
                re.search(SL_GET_TITLE_VALUE, starline) is None
                and re.match("##", starline) is None
            ):
                starline = starline.replace("\n", "")
                # Filters the titles of the tables
                if re.search(r"# ", starline):
                    block_titles.append(starline)
                # Filters the empty spaces
                elif starline != "":
                    starline = re.sub("\s{2,}", " ", starline.strip())
                    tab.append(starline.split(" "))
                # Generates a block for each empty line that founds and if 
                # the block is larger it appends it
                else:
                    if len(tab) > 1:
                        blocks.append(tab)
                        tab = []

        blocks.append(tab)
        tab = []
    first_title = (
        re.sub("\s{2,}", " ", block_titles[0][1:])
        .replace(".", "")
        .replace("?", "")
        .strip()
    )
    spectra_dict = {
        "synthetic_spectrum": QTable(
            rows=blocks[4], names=["l_obs", "f_obs",
                                   "f_syn", "weights"]
        ),
        "synthesis_results": QTable(
            rows=blocks[0], names=first_title.split(" ")
        ),
        "chains_info_xj": QTable(rows=blocks[1]),
        "chains_info_mj": QTable(rows=blocks[2]),
        "AV_chi2_Mass_ichain": QTable(
            rows=np.array(blocks[3]).T[1:],
            names=np.array(blocks[3]).T[0],
        ),
    }

    # summary_info = _make_dframe(summary_info)
    # return summary_info, spectra_dict
    return core.SpectralSummary(header=summary_info, data=spectra_dict)


def _make_dframe(dic):

    """
    Quiero que esta funcion convierta 
    un diccionario en un dataframe
    """

    data_dic = {item: dic.get(item, None) for item in dic}

    df = pd.DataFrame.from_dict(data_dic, orient="index", columns=["Value"])

    return df
