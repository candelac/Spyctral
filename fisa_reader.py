# Importamos los paquetes que necesitamos
import re

from astropy.table import Table

import pandas as pd


# Esta funcion lee el header y lo guarda en un DataFrame


def read_fisa_output_header_dataframe(path):
    """Read header of FISA output and through it to a DataFrame"""
    try:
        with open(path, "r") as fp:
            fisa_header_lines = []
            lines = fp.readlines()

            # Detectar las líneas con '#'

            for i, line in enumerate(lines):
                if re.match(r"^\s*#", line):
                    line = line.strip()  # Eliminar '\n' al final de la línea

                    # No dividir las dos primeras líneas
                    if i < 2:
                        fisa_header_lines.append({"Parameters": line, "": ""})
                    else:
                        # Buscar si la línea contiene ';'
                        if ";" in line:
                            # Dividir la línea en dos
                            # partes en el separador ';'
                            parts = line.split(";", 1)

                            # Antes de agregar a la lista, dividir
                            # cada parte por el doble espacio en blanco
                            for part in parts:
                                sub_parts = part.split("e ", 1)
                                if len(sub_parts) == 2:
                                    fisa_header_lines.append(
                                        {
                                            "Parameters": sub_parts[0].strip()
                                            + "e",
                                            "": sub_parts[1].strip(),
                                        }
                                    )
                                else:
                                    fisa_header_lines.append(
                                        {
                                            "Parameters": sub_parts[0].strip(),
                                            "": "",
                                        }
                                    )
                        else:
                            # Intentar dividir por ':'
                            parts = line.split(":", 1)

                            if len(parts) == 2:
                                # Si la línea contiene al menos un
                                # separador válido,
                                # agregar las partes a la lista
                                fisa_header_lines.extend(
                                    [{"Parameters": parts[0], "": parts[1]}]
                                )

        # Eliminar las primeras 2 y última línea
        fisa_header_lines.pop(0)
        fisa_header_lines.pop(0)
        fisa_header_lines.pop()

        # Convertir la lista de diccionarios en un DataFrame
        fisa_header = pd.DataFrame(fisa_header_lines)

        # Reemplazar el carácter '#' en todas las columnas del DataFrame
        fisa_header = fisa_header.apply(lambda x: x.str.replace("#", ""))

        return fisa_header

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {path} does not exist.")

    except IOError as e:
        raise IOError(f"Unable to open the file: {path}. Error: {str(e)}")


# Esta funcion lee el header y lo guarda un archivo de texto


def save_fisa_output_header(input_path, output_path):
    """Read header lines from the input file and
    write them to the output file."""
    try:
        with open(input_path, "r") as input_file:
            fisa_header_lines = []
            lines = input_file.readlines()

            # Detectar las líneas con '#'
            for line in lines:
                if re.match(r"^\s*#", line):
                    fisa_header_lines.append(line.strip())

        if fisa_header_lines:
            with open(output_path, "w") as output_file:
                # Escribe las líneas seleccionadas en el archivo de salida
                output_file.writelines("\n".join(fisa_header_lines))

            return f"Fisa header lines have been saved to: {output_path}"
        else:
            return 'No header lines starting with "#" found in the input file.'

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {input_path} does not exist.")

    except IOError as e:
        raise IOError(
            f"Unable to open the file: {input_path}. Error: {str(e)}"
        )


# Esta funcion separa en bloques el archivo, teniendo en cuenta las lineas
# vacias


def read_until_double_empty_lines(file_path):
    try:
        with open(file_path, "r") as file:
            blocks = []  # Lista para almacenar los bloques de texto
            empty_line_count = 0
            current_block = []

            for line in file:
                # Verifica si la línea actual está en blanco o comienza con '#'
                if line.strip() == "" or line.strip().startswith("#"):
                    empty_line_count += 1
                else:
                    empty_line_count = (
                        0  # Reinicia el contador de líneas vacías
                    )

                if empty_line_count == 2:
                    blocks.append(
                        current_block
                    )  # Agrega el bloque actual a la lista
                    current_block = []  # Reinicia el bloque actual

                # Agrega la línea al bloque actual solo si no comienza con '#'
                if not line.strip().startswith("#"):
                    current_block.append(line)

            if current_block:  # Asegúrate de agregar el último bloque
                # si no terminó con líneas vacías
                blocks.append(current_block)

            return blocks

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    except IOError as e:
        raise IOError(f"Unable to open the file: {file_path}. Error: {str(e)}")


# Esta funcion crea tablas a partir de una lista que contiene los bloques
# de archivo


def create_tables_from_blocks(blocks):
    tables = []

    for block in blocks:
        block_data = []
        column_names = [
            "Wavelength",
            "Flux",
        ]  # Nombres de columna personalizados
        for line in block:
            # Verifica si la línea comienza con '#' o está en blanco
            if not line.strip() or line.strip().startswith("#"):
                continue  # Salta líneas vacías y comentarios

            # Divide la línea en elementos usando múltiples espacios como
            # separadores
            elements = re.split(r"\s+", line.strip())

            # Convierte los elementos en números de punto flotante y crea una
            # fila de datos con formato
            formatted_line = [f"{float(element):.9f}" for element in elements]
            block_data.append(formatted_line)

        if column_names and block_data:
            table = Table(rows=block_data, names=column_names)
            tables.append(table)

    return tables


# Esta funcion renombra las tablas

# def tables_names(file_path):
#    """This function name each table"""
# No guardamos las tablas, solo las cargamos
#    tables = make_fisa_tables(file_path, save=False)
#    table_names = {
#        "Unreddened_spectrum": tables[0],
#        "Template_spectrum": tables[1],
#        "Observed_spectrum": tables[2],
#        "Residual_flux": tables[3]
#    }

#    return table_names

# Me di cuenta que podia meterlo en la otra funcion, y la re-escribi


def tables_names(tables):
    table_names = [
        "Unreddened_spectrum",
        "Template_spectrum",
        "Observed_spectrum",
        "Residual_flux",
    ]
    renamed_tables = {
        table_name: table for table_name, table in zip(table_names, tables)
    }
    return renamed_tables


# Esta funcion une la que separa en bloque y la que crea tablas
# y guarda las tablas en diferentes archivos de ser requerido


def make_fisa_tables(file_path, save=False):
    """This function makes FISA tables from an input file.


    Output:

    tendria que decir que tables[idx]
     Index 0 = Unreddened spectrum
     Index 1 = Template spectrum
     Index 2 = Observed spectrum
     Index 3 = Residual flux

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


# Aca una version completa de la funcion anterior,
# le agrege la documentacion e intente
# que los valores fueran flotantes pero no funciono


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
