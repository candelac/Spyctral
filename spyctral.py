# Importamos los paquetes que necesitamos
# import io

# import pandas as pd

# import numpy as np

import os


# Creamos la clase que define el tipo de objeto base
# La idea esque sea una súper tabla, que tenga la dimension segun cual
# sea el archivo de entrada


class SpectralSummary:
    def __init__(self, data_in):
        """This is the constructor that lets us create
        objects from this class.

        Parameters
        ----------
        data_in: diccionario con tablas adentro


        Returns
        -------
        ss: SpectralSummary instance #superTabla

        """

        self.data = data_in


# import fisa_reader


def make_fisa_tables_1(file_path, save=False):
    """This function makes FISA tables from an input file.

    Args:
        file_path (str): The path to the input FISA file.
        save (bool, optional): If True, the function will
                               save tables as text files.
            Default is False.

    Returns:
        list or str: Depending on the `save` parameter,
                     it either returns a list of
                     tables or a message about saved files.

    Example:
        The function returns tables with the following names:
        - Index 0 = Unreddened spectrum
        - Index 1 = Template spectrum
        - Index 2 = Observed spectrum
        - Index 3 = Residual flux
    """
    try:
        file_names = [
            "Unreddened_spectrum",
            "Template_spectrum",
            "Observed_spectrum",
            "Residual_flux",
        ]
        blocks = read_until_double_empty_lines(file_path)
        tables = create_tables_from_blocks(blocks)
        files_out = []

        for idx, table in enumerate(tables):
            # Convertir cada elemento de la tabla a flotantes con 9 decimales
            for column in table.colnames:
                table[column] = [
                    f"{float(value):.9f}" for value in table[column]
                ]

            if save:
                file_name = (
                    file_names[idx]
                    if idx < len(file_names)
                    else f"table_{idx}"
                )
                file_path_out = f"{file_name}.txt"
                files_out.append(file_path_out)
                with open(file_path_out, "w") as f_out:
                    table.write(f_out, format="ascii.basic")

        if save:
            return f"Each table file name saved are: {files_out}"
        else:
            # Renombrar las tablas
            tables_with_names = tables_names(tables)
            return tables_with_names

    except FileNotFoundError as e:
        return f"Error: {str(e)}. The file {file_path} does not exist."

    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


def read_fisa(filename):
    """
    Funcíon que lee archivo FISA.

    Parameters
    ----------
    filename : "str"
        Name of file

    Return
    ----------
    out : dict

    """
    assert os.path.exists(filename), "File not found"

    file = open(filename, "r")
    data_in = [k.split() for k in file.read().splitlines()]
    file.close()

    # info del header
    header = {}
    fisa = {}
    fisa["header"] = header

    header["FISA_version"] = float(data_in[1][6])
    header["date"] = data_in[2][2]
    header["time"] = data_in[2][4]
    header["redenning"] = float(data_in[3][2])
    header["template"] = data_in[4][2].split("/")[-1]
    header["normalization_point"] = float(data_in[5][3])

    # separación entre espectros
    index = found_index(data_in)

    # unreddened spectrum
    unreddened_lambda = []
    unreddened_flambda = []
    n0 = 11
    n1 = index[0]

    for i in range(n0, n1):
        unreddened_lambda.append(float(data_in[i][0]))
        unreddened_flambda.append(float(data_in[i][1]))

    fisa["unreddened_spec"] = Table()
    fisa["unreddened_spec"]["lambda"] = unreddened_lambda
    fisa["unreddened_spec"]["flux"] = unreddened_flambda

    # template spectrum
    template_lambda = []
    template_flambda = []
    n2 = index[2]

    for i in range(n1 + 2, n2):
        template_lambda.append(float(data_in[i][0]))
        template_flambda.append(float(data_in[i][1]))

    fisa["template_spec"] = Table()
    fisa["template_spec"]["lambda"] = template_lambda
    fisa["template_spec"]["flux"] = template_flambda

    # observed spectrum
    observed_lambda = []
    observed_flambda = []
    n3 = index[4]

    for i in range(n2 + 2, n3):
        observed_lambda.append(float(data_in[i][0]))
        observed_flambda.append(float(data_in[i][1]))

    fisa["observed_spec"] = Table()
    fisa["observed_spec"]["lambda"] = observed_lambda
    fisa["observed_spec"]["flux"] = observed_flambda

    # residual flux
    residual_lambda = []
    residual_flambda = []

    for i in range(n3 + 2, len(data_in)):
        residual_lambda.append(float(data_in[i][0]))
        residual_flambda.append(float(data_in[i][1]))

    fisa["residual_spec"] = Table()
    fisa["residual_spec"]["lambda"] = residual_lambda
    fisa["residual_spec"]["flux"] = residual_flambda

    return SpectralSumary(data=fisa)
