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
    Descripción en castellano:
    Convierte un encabezado dado (en forma de diccionario) en un DataFrame de pandas.

    Argumentos:
        header (dict): Diccionario que contiene las claves y valores del encabezado.

    Retorna:
        pd.DataFrame: DataFrame con las claves del encabezado como índice y los valores
            en una columna llamada "value".

    *************************************************************************************
    *************************************************************************************
    Description in English:
    Converts a given header (in dictionary form) into a pandas DataFrame.

    Arguments:
        header (dict): Dictionary containing the header keys and values.

    Returns:
        pd.DataFrame: DataFrame with header keys as the index and values in a column
            named "value".
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
    Descripción en castellano:
    Esta clase encapsula todos los datos obtenidos de un archivo de entrada.

    Atributos:
        obj_name (str): Nombre del objeto.
        header (dict): Información del encabezado del archivo de entrada.
        data (dict): Información de los espectros en formato Qtables.
        age (float): Edad del objeto.
        err_age (float): Error asociado a la edad.
        reddening (float): Valor de enrojecimiento.
        av_value (float): Valor de  "Av".
        normalization_point (float): Valor del punto de normalización.
        z_value (float): Valor de metalicidad..
        spectra (dict): Conjunto de espectros extraídos de los datos.
        extra_info (dict): Información adicional.

    *************************************************************************************
    *************************************************************************************
    Description in English:
    This class encapsulates all the data obtained from an input file.

    Attributes:
        obj_name (str): Object name.
        header (dict): Header information from the input file.
        data (dict): Spectra information in Qtables format.
        age (float): Object's age.
        err_age (float): Error associated with the age.
        reddening (float): Value of reddening.
        av_value (float): Value of "Av".
        normalization_point (float): Value of the normalization_point.
        z_value (float): Metallicity value.
        spectra (dict): Set of spectra extracted from the data.
        extra_info (dict): Additional information.
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
            Descripción en castellano:
            Convierte la información contenida en el atributo `header` a un DataFrame de
            pandas.

        Retorna:
            pd.DataFrame: DataFrame que contiene la información del encabezado, donde las
                claves del encabezado son los índices y los valores se almacenan en una
                columna llamada "value".

            *********************************************************************************
            *********************************************************************************
            Description in English:
            Converts the information stored in the `header` attribute into a pandas
            DataFrame.

            Returns:
            pd.DataFrame: DataFrame containing the header information, where the header
                keys are the index, and the values are stored in a column named "value".
        """
        return _header_to_dataframe(self.header)

    def get_spectrum(self, name: str):
        """
        Descripción en castellano:
        Obtiene un espectro específico a partir del conjunto de espectros almacenados
        en el atributo `spectra`.

        Argumentos:
            name (str): Nombre del espectro que se desea obtener.

        Retorna:
            Spectrum: El espectro correspondiente al nombre proporcionado.

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Retrieves a specific spectrum from the set of spectra stored in the `spectra`
        attribute.

        Arguments:
            name (str): Name of the spectrum to retrieve.

        Returns:
            Spectrum: The spectrum corresponding to the given name.
        """
        return self.spectra[name]

    def __getitem__(self, k: str):
        """
         Descripción en castellano:
         Permite acceder a los atributos de la clase utilizando una sintaxis similar a un
         diccionario.

        Argumentos:
            k (str): Nombre del atributo que se desea obtener.

        Retorna:
            Any: Valor del atributo solicitado.

        Lanza:
            KeyError: Si el atributo no existe.

        *************************************************************************************
        *************************************************************************************
        Description in English:
        Allows access to the class attributes using dictionary-like syntax.

        Arguments:
            k (str): Name of the attribute to retrieve.

        Returns:
            Any: Value of the requested attribute.

        Raises:
            KeyError: If the attribute does not exist.
        """
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError(k)

    def __len__(self) -> int:
        """
        Descripción en castellano:
        Retorna la cantidad de atributos definidos en la clase.

        Retorna:
            int: Número total de atributos en la clase.

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Returns the number of attributes defined in the class.

        Returns:
            int: Total number of attributes in the class.
        """

        return len(attrs.fields(SpectralSummary))

    def __repr__(self) -> str:
        """
        Descripción en castellano:
        Retorna una representación en forma de cadena de texto de la instancia de la
        clase.
        Incluye un resumen de los principales atributos: encabezado, datos, espectros e
        información adicional.

        Retorna:
            str: Representación en cadena de la instancia.

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Returns a string representation of the class instance.
        Includes a summary of the main attributes: header, data, spectra, and additional
        info.

        Returns:
            str: String representation of the instance.
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
        Descripción en castellano:
        Calcula la relación de metalicidad [Fe/H] a partir del valor Z
        (`metallicity_value`) de la instancia y una constante solar (`Z_SUN`).

        Retorna:
            float: Relación de metalicidad [Fe/H].

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Calculates the metallicity ratio [Fe/H] using the Z value (`metallicity_value`)
        of the instance and a solar constant (`Z_SUN`).

        Returns:
            float: Metallicity ratio [Fe/H].
        """
        feh_ratio = np.log10(self.z_value / Z_SUN)

        return feh_ratio

    @property
    def plot(self):
        """
        Descripción en castellano:
        Genera un objeto para graficar los espectros almacenados en la instancia.
        Utiliza la clase `SpectralPlotter` para gestionar las funcionalidades de
        graficado.

        Retorna:
            SpectralPlotter: Objeto que permite generar gráficos de los espectros.

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Generates an object for plotting the spectra stored in the instance.
        Uses the `SpectralPlotter` class to handle plotting functionalities.

        Returns:
            SpectralPlotter: Object that enables generating plots of the spectra.
        """
        from .plot import SpectralPlotter

        return SpectralPlotter(self)

    @property
    def get_all_properties(self) -> pd.DataFrame:
        """
        Descripción en castellano:
        Crea un DataFrame que contiene todos los parámetros relevantes de la instancia.
        Los valores numéricos se formatean para mostrar notación científica donde sea
        necesario.

        Retorna:
            pd.DataFrame: DataFrame con dos columnas: "Property" (propiedad) y
                "Value" (valor).

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Creates a DataFrame containing all relevant parameters of the instance.
        Numerical values are formatted to display scientific notation where necessary.

        Returns:
            pd.DataFrame: DataFrame with two columns: "Property" (property) and "Value"
                (value).
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
