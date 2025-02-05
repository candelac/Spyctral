# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.


# =============================================================================
# IMPORTS
# =============================================================================

import re

import astropy.units as u
from astropy.table import QTable

import dateutil.parser

import numpy as np

import pandas as pd

from specutils import Spectrum1D

from spyctral.core import core


# =============================================================================
# FUNCTIONS
# =============================================================================

SL_GET_HEADER = re.compile(r"\[")
SL_GET_TITLE_VALUE = re.compile(r"\[")
SL_REPLACE_AND = re.compile(r"&")
SL_GET_MULTIPLE_VALUES = re.compile(r",")
SL_GET_DATE = re.compile(r"\b\d{2}/[a-zA-Z]{3}/\d{4}\b")
PATRON = re.compile(r"#(.*?)(?:(?=\n)|$)")


def _proces_header(header_ln):
    """
    Receives a list of header lines from a Starlight file and returns a
    dictionary with the extracted parameters and values.

    Arguments:
        header_ln (list): List of strings representing the header lines.

    Returns:
        dict: Dictionary where keys are parameter names and values are the
            extracted values from the header.
    """

    head_dict = {}
    for sl in header_ln:
        if re.findall(SL_GET_DATE, sl):
            head_dict["Date"] = dateutil.parser.parse(
                re.findall(SL_GET_DATE, sl)[0]
            )

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
                    head_dict[
                        starline_var[pos]
                        .strip()
                        .split(" ")[0]
                        .replace("-", "_")
                    ] = float(val)
                else:
                    head_dict[
                        starline_var[pos]
                        .strip()
                        .split(" ")[0]
                        .replace("-", "_")
                    ] = val

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


def _is_float(element: any) -> bool:
    """
    Checks whether a given element can be converted to a floating-point number.

    Arguments:
        element (any): Element to check.

    Returns:
        bool: `True` if the element can be converted to a floating-point
            number, `False` otherwise.
    """
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def _proces_tables(block_lines):
    """
    Processes the data block lines of a Starlight file and returns a dictionary
    with four structured tables containing key information, such as the
    synthetic spectrum and results.

    Arguments:
        block_lines (list): List of strings representing the data block lines.

    Returns:
        dict: A dictionary with the following keys and values:
            - "synthetic_spectrum" (QTable): Table with the columns "l_obs",
                "f_obs", "f_syn", and "weights".
            - "synthetic_results" (QTable): Table with synthetic results.
            - "results_average_chains_xj" (QTable): Table with averages of
                x_j chains.
            - "results_average_chains_mj" (QTable): Table with averages of
                m_j chains.
            - "results_average_chains_Av_chi2_mass" (QTable): Table with
                average values of Av, chi^2, and mass.
    """
    block_titles = []
    blocks = []
    tab = []
    for sl in block_lines:
        # This part procces the tables.
        if (
            re.search(SL_GET_TITLE_VALUE, sl) is None
            and re.match("##", sl) is None
        ):
            # Filters the titles of the tables.
            if re.search(r"# ", sl):
                block_titles.append(sl)
            # Filters the empty spaces
            elif len(sl) > 1:
                sl = re.sub(r"\s{2,}", " ", sl.strip())
                tab.append(sl.split(" "))

            # Generates a block for each empty line that founds
            # and if the block is larger it appends it
            else:
                if len(tab) >= 1:
                    blocks.append(tab)
                    tab = []
    blocks.append(tab)
    tab = []
    first_title = (
        re.sub(r"\s{2,}", " ", block_titles[0][1:])
        .replace(".", "")
        .replace("?", "")
        .strip()
    ).split(" ")
    # Take the units from the headers and remove the '()'
    unities = []
    clean_title = []
    for t in first_title:
        splited = t.split("(")
        if len(splited[0]) > 0:
            clean_title.append(splited[0])
        else:
            clean_title.append(splited[1].split(")")[1])

        if len(splited) >= 2:
            if splited[1].split(")")[0] == "%":
                unities.append(splited[1].split(")")[0])
            else:
                unities.append("")
        else:
            unities.append("")

    # Verificar que los elementos sean numeros
    for ibl, lin in enumerate(blocks):
        for i, row in enumerate(blocks[ibl]):
            converted_row = []
            for item in row:
                if _is_float(item):  # Solo convierte si es un número flotante
                    converted_item = float(item)
                    converted_row.append(converted_item)
                else:
                    converted_row.append(item)  # Si no se puede convertir, deja el valor original
            blocks[ibl][i] = converted_row


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
            rows=blocks[0], names=clean_title, units=unities
        ),
        "results_average_chains_xj": QTable(rows=blocks[1]),
        "results_average_chains_mj": QTable(rows=blocks[2]),
        "results_average_chains_Av_chi2_mass": QTable(
            rows=np.array(blocks[3]).T[1:],
            names=["AV", "ch2", "Mass"],
        ),
    }

    return spectra_dict


def _get_ssp_contributions(tables_dict, xj_percent):
    """
    Calculates the contributions of Single Stellar Populations (SSPs)
    from the synthetic results, filtering those contributions greater
    than a given percentage and normalizing the values.

    Arguments:
        tables_dict (dict): Dictionary containing processed tables, including
            "synthetic_results".
        xj_percent (float): Minimum percentage to filter contributions
            (e.g., 5 means 5%).

    Returns:
        pandas.DataFrame: DataFrame with the filtered and normalized SSP
            contributions. Includes columns like "x_j" (normalized percentages)
            and "age_j" (stellar population ages).
    """

    ssps_vector = tables_dict["synthetic_results"]
    ssps_vector = (
        ssps_vector.to_pandas()
    )  # Convertir QTable a DataFrame de Pandas

    # Convertir todas las columnas a números flotantes
    ssps_vector = ssps_vector.apply(pd.to_numeric, errors="coerce")

    ssps_vector = ssps_vector[ssps_vector["x_j"] > xj_percent].reset_index(
        drop=True
    )
    ssps_vector["x_j"] = (ssps_vector["x_j"] * 100) / ssps_vector["x_j"].sum()

    return ssps_vector


def _get_age(ssps_vector, age_decimals):
    """
    Calculates the weighted average age of stellar populations (SSPs)
    using the normalized contributions (x_j) and SSP ages (age_j).

    Arguments:
        ssps_vector (pandas.DataFrame): DataFrame containing SSP contributions.
            Must include the columns "x_j" (normalized contributions) and
            "age_j" (SSP ages).
        age_decimals (int): Number of decimals to round the calculated age.

    Returns:
        float: The weighted average age of the SSPs, rounded to the specified
            number of decimals.
    """
    age = ((ssps_vector["x_j"] * ssps_vector["age_j"]).sum()) / (
        ssps_vector["x_j"].sum()
    )

    age = round(age, age_decimals)

    return age


def _get_log_age(ssps_vector, age_decimals):
    """
    Calculates the base-10 logarithm of the weighted average age of
    stellar populations (SSPs), using the normalized contributions (x_j)
    and SSP ages (age_j).

    Arguments:
        ssps_vector (pandas.DataFrame): DataFrame containing SSP
            contributions. Must include the columns "x_j" (normalized
            contributions) and "age_j" (SSP ages).
        age_decimals (int): Number of decimals to round the calculated
            logarithm of the age.

    Returns:
        float: The base-10 logarithm of the weighted average age of the SSPs,
        rounded to the specified number of decimals.
    """

    l_age = ((ssps_vector["x_j"] * np.log10(ssps_vector["age_j"])).sum()) / (
        ssps_vector["x_j"].sum()
    )

    l_age = round(l_age, age_decimals)

    return l_age


def _get_error_age(ssps_vector, age, age_decimals):
    """
    Calculates the error associated with the weighted average age of stellar
    populations (SSPs).
    This error is based on the weighted variance of the SSP ages.

    Arguments:
        ssps_vector (pandas.DataFrame): DataFrame containing SSP contributions.
            Must include the columns "x_j" (normalized contributions) and
            "age_j" (SSP ages).
        age (float): Calculated weighted average age.
        age_decimals (int): Number of decimals to round the calculated error.

    Returns:
        float: The error associated with the weighted average age of the SSPs,
        rounded to the specified number of decimals.
    """

    desviaciones_cuadradas_2 = (
        ssps_vector["x_j"] * (ssps_vector["age_j"] - age) ** 2
    )

    suma_ponderada_desviaciones_cuadradas_2 = np.sum(desviaciones_cuadradas_2)

    suma_pesos = np.sum(ssps_vector["x_j"])

    varianza_ponderada_2 = suma_ponderada_desviaciones_cuadradas_2 / suma_pesos

    err_age = np.sqrt(varianza_ponderada_2)

    err_age = round(err_age, age_decimals)

    return err_age


def _get_reddening(header_info, rv):
    """
    Determines the reddening value and extinction value (A_v)
    from the header information and the R_v parameter.

    Arguments:
        header_info (dict): Dictionary containing the file header information.
            Must include the key "AV_min" for the minimum extinction value.
        rv (float): Reddening parameter (R_v), typically 3.1 for the
            interstellar medium.

    Returns:
        tuple:
            - reddening_value (float): Reddening value calculated as A_v / R_v.
            - av_value (float): Extinction value A_v extracted from the header.
    """

    av_value = header_info["AV_min"]
    reddening_value = av_value / rv

    return reddening_value, av_value


def _get_metallicity(ssps_vector, z_decimals):
    """
    Calculates the weighted average metallicity (Z) of stellar populations
    (SSPs), using the normalized contributions (x_j) and metallicity values
    (Z_j).

    Arguments:
        ssps_vector (pandas.DataFrame): DataFrame containing SSP contributions.
            Must include the columns "x_j" (normalized contributions) and "Z_j"
            (SSP metallicities).
        z_decimals (int): Number of decimals to round the calculated
            metallicity value.

    Returns:
        float: The weighted average metallicity (Z), rounded to the specified
        number of decimals.
    """

    z_value = ((ssps_vector["x_j"] * ssps_vector["Z_j"])).sum() / ssps_vector[
        "x_j"
    ].sum()
    z_value = round(z_value, z_decimals)

    return z_value


def _get_z_values(ssps_vector):
    """
    Retrieves the maximum and minimum metallicity (Z) values of stellar
    populations (SSPs), based on the normalized contributions (x_j).

    Arguments:
        ssps_vector (pandas.DataFrame): DataFrame containing SSP contributions.
            Must include the columns "x_j" (normalized contributions) and "Z_j"
            (SSP metallicities).

    Returns:
        dict: A dictionary with the maximum and minimum metallicity values:
            - `z_ssp_max` (float): Maximum metallicity value.
            - `z_ssp_min` (float): Minimum metallicity value.
    """
    max_xj_index = ssps_vector["x_j"].idxmax()
    min_xj_index = ssps_vector["x_j"].idxmin()

    z_ssp_max = float(ssps_vector.loc[max_xj_index, "Z_j"])
    z_ssp_min = float(ssps_vector.loc[min_xj_index, "Z_j"])

    z_values = {"z_ssp_max": z_ssp_max, "z_ssp_min": z_ssp_min}

    return z_values


def _get_vel_values(header_info):
    """
    Extracts the minimum velocity (v0_min) and minimum velocity dispersion
    (vd_min) from the header information.

    Arguments:
        header_info (dict): Dictionary containing the Starlight file header
            information. Must include the keys "v0_min" (minimum velocity)
            and "vd_min" (minimum velocity dispersion).

    Returns:
        dict: A dictionary with the extracted velocity values:
            - `v0_min` (float): Minimum velocity.
            - `vd_min` (float): Minimum velocity dispersion.
    """
    v0_min = float(header_info["v0_min"])
    vd_min = float(header_info["vd_min"])

    vel_values = {"v0_min": v0_min, "vd_min": vd_min}

    return vel_values


def _get_quality_fit_values(header_info):
    """
    Extracts values related to the model's fit quality, such as the effective
    chi-square (chi2_Nl_eff) and the average absolute deviation (adev), from
    the header information.

    Arguments:
        header_info (dict): Dictionary containing the Starlight file header
            information. Must include the keys "chi2_Nl_eff" (effective
            chi-square) and "adev" (average absolute deviation).

    Returns:
        dict: A dictionary with the fit quality values:
            - `chi2_nl_eff` (float): Effective chi-square value.
            - `adev` (float): Average absolute deviation.
    """
    chi2_nl_eff = float(header_info["chi2_Nl_eff"])
    adev = float(header_info["adev"])

    quality_fit = {"chi2_nl_eff": chi2_nl_eff, "adev": adev}

    return quality_fit


def _get_starlight_extra_info(ssps_vector, header_info):
    """
    Gathers additional Starlight-specific information, such as metallicity
    (Z) values, velocities, and model fit quality, and organizes it into
    a DataFrame.

    Arguments:
        ssps_vector (pandas.DataFrame): DataFrame containing SSP contributions.
            Includes columns like "x_j" (normalized contributions) and "Z_j"
            (metallicities).
        header_info (dict): Dictionary containing the Starlight file header
            information. Must include keys such as "v0_min", "vd_min",
            "chi2_Nl_eff", and "adev".

    Returns:
        pandas.DataFrame: A DataFrame containing Starlight-specific
            information.
            Rows include values such as:
                - `z_ssp_max`: Maximum metallicity value.
                - `z_ssp_min`: Minimum metallicity value.
                - `v0_min`: Minimum velocity.
                - `vd_min`: Minimum velocity dispersion.
                - `chi2_nl_eff`: Effective chi-square value.
                - `adev`: Average absolute deviation.
    """
    z_values = _get_z_values(ssps_vector)
    vel_values = _get_vel_values(header_info)
    quality_fit = _get_quality_fit_values(header_info)

    keys = (
        list(z_values.keys())
        + list(vel_values.keys())
        + list(quality_fit.keys())
    )
    values = (
        list(z_values.values())
        + list(vel_values.values())
        + list(quality_fit.values())
    )

    starlight_particular_info = pd.DataFrame(values, index=keys)

    return starlight_particular_info


def _make_spectrum1d_from_qtable(qtable):
    """
    Creates `Spectrum1D` objects from a `QTable` containing data for
    synthetic, observed, and residual spectra.

    Arguments:
        qtable (QTable): Table containing the columns:
            - "l_obs": Observed wavelength.
            - "f_obs": Observed flux.
            - "f_syn": Synthetic flux.
            - "weights": Weights used in the calculation.

    Returns:
        dict: A dictionary with the `Spectrum1D` objects created from
            the table data:
                - `synthetic_spectrum`: Synthetic spectrum.
                - `observed_spectrum`: Observed spectrum.
                - `residual_spectrum`: Residual spectrum calculated as
                    (f_obs - f_syn) / f_obs.
    """

    # Extract the necessary columns
    wavelength = qtable["l_obs"]
    flux_obs = qtable["f_obs"].data  # Extract data without units
    flux_syn = qtable["f_syn"].data  # Extract data without units

    # Calculate the residual flux
    # residual_flux = (flux_obs - flux_syn) / flux_obs
    residual_flux = flux_obs - flux_syn

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


def _get_spectra(data):
    """
    Generates `Spectrum1D` spectra from the provided tabular data.
    If the dictionary contains a "synthetic_spectrum" table with the
    necessary columns, it uses `_make_spectrum1d_from_qtable` to create
    the spectra.

    Arguments:
        data (dict): Dictionary containing tabular data. Keys represent
            table names, and values are `QTable` objects.

    Returns:
        dict: A dictionary containing the generated `Spectrum1D` objects.
            Keys include:
                - `synthetic_spectrum`: Synthetic spectrum.
                - `observed_spectrum`: Observed spectrum.
                - `residual_spectrum`: Residual spectrum.
    """
    spectra = {}
    for key, value in data.items():
        if len(value.columns) == 4 and key == "synthetic_spectrum":
            spectra = _make_spectrum1d_from_qtable(value)

    return spectra


def read_starlight(
    path,
    *,
    xj_percent=5,
    age_decimals=2,
    rv=3.1,
    z_decimals=3,
    object_name="object_1",
):
    """
    Processes a Starlight file, extracting the header, data tables, and
    key values such as age, metallicity, and reddening. Returns a spectral
    summary with all processed information.

    Arguments:
        path (str): Path to the Starlight file to process.
        xj_percent (float, optional): Minimum SSP contribution percentage to
            include in the calculation. Default: 5.
        age_decimals (int, optional): Number of decimals to round age
            calculations. Default: 2.
        rv (float, optional): Reddening parameter (R_v). Default: 3.1.
        z_decimals (int, optional): Number of decimals to round metallicity
            calculations. Default: 3.
        object_name (str, optional): Name of the analyzed object.
            Default: "object_1".

    Returns:
        core.SpectralSummary: An object encapsulating the spectral summary,
            including:
                - Processed header.
                - Generated `Spectrum1D` spectra.
                - Key values like age, metallicity, and reddening.
                - Processed tables with results.
    """

    obj_name = object_name

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

    err_age = _get_error_age(ssps_vector, age, age_decimals)

    reddening_value, av_value = _get_reddening(header_info, rv)

    normalization_point = header_info["l_norm"]

    z_value = _get_metallicity(ssps_vector, z_decimals)

    synthesis_info = _get_starlight_extra_info(ssps_vector, header_info)

    spectra = _get_spectra(tables_dict)

    l_age = _get_log_age(ssps_vector, age_decimals)

    extra_info = {
        "xj_percent": xj_percent,
        "age_decimals": age_decimals,
        "rv": rv,
        "z_decimals": z_decimals,
        "ssps_vector": ssps_vector,
        "synthesis_info": synthesis_info,
        "average_log_age": l_age,
    }

    return core.SpectralSummary(
        obj_name=obj_name,
        header=header_info,
        data=tables_dict,
        age=age,
        err_age=err_age,
        reddening=reddening_value,
        av_value=av_value,
        normalization_point=normalization_point,
        z_value=z_value,
        spectra=spectra,
        extra_info=extra_info,
    )
