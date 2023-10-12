import os

import astropy.units as u
from astropy.table import QTable


class SpectralSummary:
    def __init__(self, filename, reader):
        self.filename = filename

        if reader == "fisa":
            self.fisa = read_fisa(self.filename)
        elif reader == "starlight":
            self.starlight = read_starlight(self.filename)
        else:
            print("Reader not found")


# Funciones de lectura


def read_fisa(filename):
    """
    Función que lee archivo FISA.

    Parameters
    ----------
    filename : "str"
        Name of file

    Return
    ----------
    fisa : dict

    """
    assert os.path.exists(filename), "File not found"

    file = open(filename, "r")
    data_in = [k.split() for k in file.read().splitlines()]
    file.close()

    # info del header
    fisa = {}
    header = {}
    fisa["header"] = header

    header["FISA_version"] = float(data_in[1][6])
    header["date"] = data_in[2][2]
    header["time"] = data_in[2][4]
    header["redenning"] = float(data_in[3][2])
    header["template"] = data_in[4][2].split("/")[-1]
    header["normalization_point"] = float(data_in[5][3])

    # separación entre espectros
    index = []
    for idx, elemento in enumerate(data_in):
        if len(data_in[idx]) == 0:
            index.append(idx)

    # unreddened spectrum
    unreddened_lambda = []
    unreddened_flambda = []
    n0 = 11
    n1 = index[0]

    for i in range(n0, n1):
        unreddened_lambda.append(float(data_in[i][0]))
        unreddened_flambda.append(float(data_in[i][1]))

    fisa["unreddened_spec"] = QTable()
    fisa["unreddened_spec"]["wavelength"] = unreddened_lambda * u.Angstrom
    fisa["unreddened_spec"]["flux"] = unreddened_flambda

    # template spectrum
    template_lambda = []
    template_flambda = []
    n2 = index[2]

    for i in range(n1 + 2, n2):
        template_lambda.append(float(data_in[i][0]))
        template_flambda.append(float(data_in[i][1]))

    fisa["template_spec"] = QTable()
    fisa["template_spec"]["wavelength"] = template_lambda * u.Angstrom
    fisa["template_spec"]["flux"] = template_flambda

    # observed spectrum
    observed_lambda = []
    observed_flambda = []
    n3 = index[4]

    for i in range(n2 + 2, n3):
        observed_lambda.append(float(data_in[i][0]))
        observed_flambda.append(float(data_in[i][1]))

    fisa["observed_spec"] = QTable()
    fisa["observed_spec"]["wavelength"] = observed_lambda * u.Angstrom
    fisa["observed_spec"]["flux"] = observed_flambda

    # residual flux
    residual_lambda = []
    residual_flambda = []

    for i in range(n3 + 2, len(data_in)):
        residual_lambda.append(float(data_in[i][0]))
        residual_flambda.append(float(data_in[i][1]))

    fisa["residual_spec"] = QTable()
    fisa["residual_spec"]["wavelength"] = residual_lambda * u.Angstrom
    fisa["residual_spec"]["flux"] = residual_flambda

    return fisa  # SpectralSumary(fisa)


# def read_starlight(path, **):
# leer al archivo en formato starlight
# saca estadisticos utiles para Sepectral sumary
# crea el espectral sumary

#   return SpectralSumary(....)
