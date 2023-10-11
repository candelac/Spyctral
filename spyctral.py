# Importamos los paquetes que necesitamos
# import io

# import pandas as pd

# import numpy as np

# import re


# Creamos la clase que define el objeto base
'''
class SpectralSummary(object):
    def __init__(self, filepath):
        """This is the constructor that lets us create
        objects from this class.

        Parameters
        ----------
        filepath: string
            file path of the file output

        Returns
        -------
        ss: SpectralSummary instance #superTabla

        """
        self.path = os.path.join(filepath)
        file_name, extention_file = os.path.splitext(filepath)
        self.file_name = file_name
        self.extention_file = extention_file

        try:
            # Leer el archivo

            with open(self.path, "r") as file:
                lines = file.readlines()
                print(f"Este archivo tiene: {len(lines)}.")

                # Identifico el archivo para saber cómo leerlo

                if self.extention_file == ".fisa":
                    self.fisa_object = print(
                        "Aún estamos preparando el lector, sea paciente :) "
                    )
                    # self.fisa_object = read_fisa(file)
                elif extention_file == ".out":
                    self.starlight_object = print(
                        "Aún estamos preparando el lector, sea paciente :) "
                    )
                    # self.starlight_object = read_starlight(file)

        except FileNotFoundError:
            raise (
                FileNotFoundError(f"El archivo {self.file_name} no existe.")
            )

        except IOError:
            raise (IOError(f"No se pudo abrir el archivo: {self.file_name}."))

'''

# Hago una funcion que lea el archivo de Fisa
# Deberia poder llmar el archivo donde esta todo lo que
# necesita para funcionar la make (fisa_reader.py)

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
