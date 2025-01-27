# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# This file process
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

"""
FISA_RX_VERSION.
Descripción en castellano:

Esta expresión regular extrae la versión de FISA desde el encabezado del archivo.
Captura una línea como: SPECTRUM ANALYZED WITH FISA v. 0.92.

*****************************************************************************************
*****************************************************************************************
Description in English:

This regular expression extracts the FISA version from the file header.
Captures a line like: SPECTRUM ANALYZED WITH FISA v. 0.92.
"""
FISA_RX_VERSION = re.compile(
    r"SPECTRUM ANALYZED WITH FISA v\.\s+(?P<value>[\d.][^\n]+)"
)


"""
FISA_RX_DATE_AND_TIME
Descripción en castellano:

Esta expresión regular extrae la fecha y la hora del análisis.
Captura una línea como: Date 07/09/2022; time 10:11:03.

*****************************************************************************************
*****************************************************************************************
Description in English:

This regular expression extracts the date and time of the analysis.
Captures a line like: Date 07/09/2022; time 10:11:03.
"""
FISA_RX_DATE_AND_TIME = re.compile(
    r"Date (?P<date>\d{2}/\d{2}/\d{4}); time (?P<time>\d{2}:\d{2}:\d{2})"
)


"""
FISA_RX_REDDENING
Descripción en castellano:

Extrae el valor del enrojecimiento (Reddening) desde el encabezado del archivo.
Captura una línea como: Reddening: 0.14.

*****************************************************************************************
*****************************************************************************************
Description in English:

Extracts the reddening value from the file header.
Captures a line like: Reddening: 0.14.
"""
FISA_RX_REDDENING = re.compile(r"Reddening:\s+(?P<value>[\d.][^\n]+)")


"""
FISA_RX_TEMPLATE
Descripción en castellano:

Extrae la ruta de la plantilla adoptada desde el encabezado del archivo.
Captura una línea como: Adopted Templated: /path/to/template.dat.

*****************************************************************************************
*****************************************************************************************
Description in English:

Extracts the path of the adopted template from the file header.
Captures a line like: Adopted Templated: /path/to/template.dat.
"""
FISA_RX_TEMPLATE = re.compile(r"Adopted Templated:\s*(?P<ruta>[\S]+)")


"""
FISA_RX_NORMALIZATION_POINT
Descripción en castellano:

Extrae el punto de normalización desde el encabezado del archivo.
Captura una línea como: Normalization Point: 5535.87988.

*****************************************************************************************
*****************************************************************************************
Description in English:

Extracts the normalization point from the file header.
Captures a line like: Normalization Point: 5535.87988."""
FISA_RX_NORMALIZATION_POINT = re.compile(
    r"Normalization Point:\s+(?P<value>[\d.][^\n]+)"
)


"""
FISA_RX_SPECTRA_NAMES
Descripción en castellano:

Extrae los nombres de los espectros y sus índices desde el encabezado del archivo.
Captura una línea como: Index 0 = Unreddened spectrum.

*****************************************************************************************
*****************************************************************************************
Description in English:

Extracts the spectrum names and their indices from the file header.
Captures a line like: Index 0 = Unreddened spectrum.
"""
FISA_RX_SPECTRA_NAMES = re.compile(r"Index (?P<index>\d) = (?P<value>[^\n]+)")


"""
FISA_DEFAULT_AGE_MAP
Descripción en castellano:

Define valores de edad (en años) para cada plantilla espectral. Por ejemplo:
    "G1": 13e9 → 13 mil millones de años.
    "ya_lmc": 3e6 → 3 millones de años.

*****************************************************************************************
*****************************************************************************************
Description in English:

Defines age values (in years) for each spectral template. For example:
    "G1": 13e9 → 13 billion years.
    "ya_lmc": 3e6 → 3 million years.
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
Descripción en castellano:

Define errores en los valores de edad (en años) para cada plantilla espectral.
Por ejemplo:
    "G1": 1e9 → Error de 1 mil millones de años.

*****************************************************************************************
*****************************************************************************************
Description in English:

Defines errors in age values (in years) for each spectral template. For example:
    "G1": 1e9 → Error of 1 billion years.

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
Descripción en castellano:

Define valores de metalicidad para cada plantilla espectral. Por ejemplo:
    "G1": 1.00 → Metalicidad solar.
    "G5": -1.9 → Metalicidad baja.

*****************************************************************************************
*****************************************************************************************
Description in English:

Defines metallicity values for each spectral template. For example:
    "G1": 1.00 → Solar metallicity.
    "G5": -1.9 → Low metallicity.
"""
FISA_DEFAULT_Z_MAP = {
    "G1": 1.00,
    "G2": -0.4,
    "G3": -1.0,
    "G4": -1.5,
    "G5": -1.9,
    "ya_lmc": 0.42,
    "yba_be": 0.42,
    "Ya1": 1.0,
}


def _process_header(lines):
    """
    Descripción en castellano:
    Esta función procesa las líneas del encabezado de un archivo FISA y extrae
    información clave, como la versión de FISA, la fecha, el enrojecimiento,
    la plantilla adoptada, el punto de normalización y los nombres de los espectros.

    Argumentos:
        lines (list): Lista de cadenas de texto que representan las líneas del encabezado
        del archivo FISA.

    Retorna:
        dict: Diccionario con la siguiente información:
            - 'fisa_version' (str): Versión de FISA utilizada.
            - 'date_time' (datetime): Fecha y hora del análisis.
            - 'reddening' (float): Valor de enrojecimiento.
            - 'adopted_template' (str): Ruta de la plantilla adoptada.
            - 'normalization_point' (float): Punto de normalización.
            - 'spectra_names' (tuple): Nombres de los espectros, indexados por posición.

    *************************************************************************************
    *************************************************************************************
    Description in English:
    This function processes the header lines of a FISA file and extracts
    key information, such as the FISA version, date, reddening value, adopted template,
    normalization point, and spectrum names.

    Arguments:
        lines (list): List of strings representing the header lines of the FISA file.

    Returns:
        dict: Dictionary containing the following information:
            - 'fisa_version' (str): Version of FISA used.
            - 'date_time' (datetime): Date and time of the analysis.
            - 'reddening' (float): Reddening value.
            - 'adopted_template' (str): Path of the adopted template.
            - 'normalization_point' (float): Normalization point.
            - 'spectra_names' (tuple): Spectrum names indexed by position.
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
    Descripción en castellano:
        Renombra las tablas espectrales asociando cada espectro con su nombre
        correspondiente, basado en una lista de nombres de tabla.

    Argumentos:
        spectra (list): Lista de tablas espectrales (objetos `QTable`) procesadas.
        table_names (tuple): Tupla de cadenas con los nombres asociados a cada espectro.

    Retorna:
        dict: Un diccionario donde las claves son los nombres de las tablas y los valores
        son las tablas espectrales correspondientes.

    *************************************************************************************
    *************************************************************************************
    Description in English:
        Renames the spectral tables by associating each spectrum with its corresponding
        name, based on a list of table names.

    Arguments:
        spectra (list): List of spectral tables (`QTable` objects) processed.
        table_names (tuple): Tuple of strings representing the names associated with
            each spectrum.

    Returns:
        dict: A dictionary where the keys are table names and the values
        are the corresponding spectral tables.
    """
    renamed_spectra = {
        table_name: table for table_name, table in zip(table_names, spectra)
    }
    return renamed_spectra


def _process_blocks(spectra_blocks, tab_names):
    """
    Descripción en castellano:
        Procesa los bloques de datos espectrales extraídos de un archivo FISA y los
        convierte en tablas estructuradas con columnas para longitud de onda y flujo
        normalizado.

    Argumentos:
        spectra_blocks (list): Lista de bloques espectrales, donde cada bloque contiene
        líneas de datos en formato texto.
        tab_names (tuple): Tupla de cadenas que representan los nombres asociados a cada
        espectro.

    Retorna:
        dict: Un diccionario donde las claves son los nombres de las tablas (tab_names)
        y los valores son tablas espectrales (`QTable`) con las siguientes columnas:
            - "Wavelength" (con unidad de longitud de onda en Angstroms).
            - "Normalizated_flux" (flujo normalizado).

    *************************************************************************************
    *************************************************************************************
    Description in English:
        Processes spectral data blocks extracted from a FISA file and converts them
        into structured tables with columns for wavelength and normalized flux.

    Arguments:
        spectra_blocks (list): List of spectral blocks, where each block contains lines
            of text-formatted data.
        tab_names (tuple): Tuple of strings representing the names associated with each
            spectrum.

    Returns:
        dict: A dictionary where keys are table names (tab_names) and values are spectral
            tables (`QTable`) with the following columns:
            - "Wavelength" (with unit of wavelength in Angstroms).
            - "Normalizated_flux" (normalized flux).
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
    Descripción en castellano:
        Extrae el nombre del archivo de la plantilla adoptada (template) desde el
        encabezado.

    Argumentos:
        header (dict): Diccionario que contiene la información del encabezado del
            archivo FISA, incluyendo la ruta completa de la plantilla adoptada en
            la clave 'adopted_template'.

    Retorna:
        str: El nombre del archivo de la plantilla adoptada (incluyendo su extensión).

    *************************************************************************************
    *************************************************************************************
    Description in English:
        Extracts the filename of the adopted template from the header.

    Arguments:
        header (dict): Dictionary containing the header information of the FISA file,
        including the full path of the adopted template in the 'adopted_template' key.

    Returns:
        str: The filename of the adopted template (including its extension).
    """
    template = header["adopted_template"]
    str_template = template.split("/")[-1]

    return str_template


def _get_name_template(header):
    """
    Descripción en castellano:
        Obtiene el nombre base de la plantilla adoptada desde el encabezado del archivo
        FISA.  El nombre base es el nombre del archivo sin la extensión.

    Argumentos:
        header (dict): Diccionario que contiene la información del encabezado del archivo
        FISA, incluyendo la ruta completa de la plantilla adoptada en la clave
        'adopted_template'.

    Retorna:
        str: El nombre base de la plantilla adoptada (sin extensión).

    *************************************************************************************
    *************************************************************************************
    Description in English:
    Retrieves the base name of the adopted template from the header of the FISA file.
    The base name is the filename without the extension.

    Arguments:
        header (dict): Dictionary containing the header information of the FISA file,
        including the full path of the adopted template in the 'adopted_template' key.

    Returns:
        str: The base name of the adopted template (without extension).
    """
    template = header["adopted_template"]
    name_template = (template.split("/")[-1]).split(".")[0]

    return name_template


def _get_reddening(header, rv):
    """
    Descripción en castellano:
        Calcula el valor de enrojecimiento (reddening) y su equivalente en magnitud de
        extinción (A_v), basado en el valor proporcionado en el encabezado del archivo
        FISA y el parámetro de enrojecimiento (R_v).

    Argumentos:
        header (dict): Diccionario que contiene la información del encabezado del archivo
            FISA.
        rv (float): Valor del parámetro de enrojecimiento (R_v), típicamente 3.1 para el
            medio interestelar.

    Retorna:
        tuple:
            - reddening_value (float): Valor de enrojecimiento extraído del encabezado.
            - av_value (float): Valor de magnitud de extinción (A_v) calculado como
                reddening_value * R_v.

    *************************************************************************************
    *************************************************************************************
    Description in English:
        Calculates the reddening value and its equivalent extinction magnitude (A_v),
        based on the value provided in the FISA file header and the reddening parameter
        (R_v).

    Arguments:
        header (dict): Dictionary containing the header information of the FISA file.
        rv (float): Reddening parameter (R_v), typically 3.1 for the interstellar medium.

    Returns:
        tuple:
            - reddening_value (float): Reddening value extracted from the header.
            - av_value (float): Extinction magnitude (A_v) calculated as reddening_value
                * R_v.
    """

    reddening_value = header["reddening"]
    av_value = reddening_value * rv

    return reddening_value, av_value


def _get_spectra(data):
    """
    Descripción en castellano:
        Convierte los datos espectrales procesados en un diccionario de objetos
        `Spectrum1D`, que representan espectros con longitud de onda y flujo.

    Argumentos:
        data (dict): Diccionario donde las claves son los nombres de los espectros y los
            valores son tablas espectrales (`QTable`) con columnas de longitud de onda y
            flujo normalizado.

    Retorna:
        dict: Un diccionario donde las claves son los nombres de los espectros y los
            valores son objetos `Spectrum1D` que contienen los datos de flujo y longitud
            de onda.

    *************************************************************************************
    *************************************************************************************
    Description in English:
    Converts the processed spectral data into a dictionary of `Spectrum1D` objects,
    representing spectra with wavelength and flux.

    Arguments:
        data (dict): Dictionary where keys are spectrum names and values are spectral
            tables (`QTable`) with columns for wavelength and normalized flux.

    Returns:
        dict: A dictionary where keys are spectrum names and values are `Spectrum1D`
        objects containing the flux and wavelength data.
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
    Descripción en castellano:
    Lee un archivo FISA y extrae los datos del espectro, incluyendo el encabezado y las
    columnas de datos.

    Argumentos:
        nombre_archivo (str): Ruta y nombre del archivo FISA a leer.

        age_map : dict or None, opcional
            Diccionario que mapea los valores de edad.
            Si es None, el valor por defecto es FISA_DEFAULT_AGE_MAP.
            (por defecto es None)

        rv : float, opcional
            Valor de enrojecimiento usado para los cálculos.
            (valor por defecto es 3.1)

        z_map : dict or None, opcional
            Diccionario que mapea los valores de metalicidad.
            Si es None, por defecto se toma FISA_DEFAULT_Z_MAP.
            (por defecto es None)

    Retorna:
        SpectralSummary:
            Objecto que contiene los datos encapsulados extraídos del archivo .FISA
        dict: Un diccionario con las siguientes claves:
            - 'header' (list): Líneas del encabezado del archivo.
            - 'data' (ndarray): Datos del espectro en formato NumPy array.
            - 'reddening' (float): Valor de enrojecimiento extraído del encabezado.
            - 'template' (str): Ruta de la plantilla utilizada, extraída del encabezado.
            - 'norm_point' (float): Punto de normalización extraído del encabezado.

    Notas:
        Esta función procesa un archivo FISA, extrayendo información del encabezado y
        bloques de espectros.
        Calcula la edad, el enrojecimiento, el valor AV, el punto de normalización y
        los valores de metalicidad según los datos proporcionados o predeterminados.

    *************************************************************************************
    *************************************************************************************
    Description in English:
    Reads a FISA file and extracts the spectral data, including the header and data
    columns.

    Arguments:
        nombre_archivo (str): Path and name of the FISA file to read.

        age_map : dict or None, optional
            Mapping dictionary for age values.
            If None, defaults to FISA_DEFAULT_AGE_MAP.
            (default is None)

        rv : float, optional
            Reddening value to use for calculations.
            (default is 3.1)

        z_map : dict or None, optional
            Mapping dictionary for metallicity values.
            If None, defaults to FISA_DEFAULT_Z_MAP.
            (default is None)

    Returns:
        SpectralSummary:
            Object containing encapsulated data extracted from the FISA file.
        dict: A dictionary with the following keys:
            - 'header' (list): Lines of the file's header.
            - 'data' (ndarray): Spectral data in NumPy array format.
            - 'reddening' (float): Reddening value extracted from the header.
            - 'template' (str): Path of the template used, extracted from the header.
            - 'norm_point' (float): Normalization point extracted from the header.

    Notes:
        This function processes a FISA file, extracting header information and spectra
        blocks.
        It computes age, reddening, AV value, normalization point, and metallicity values
        based on the provided or default mappings.
    """
    # Use default mappings if None provided
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
