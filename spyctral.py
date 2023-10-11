import os

from astropy.table import Table


# Creamos la clase que define el objeto base
class SpectralSummary:
    def __init__(self, filename, fisa):
        self.filename = filename

    # def plot(self):


# Funciones de lectura


def read_fisa(filename):
    # leer al archivo en formato fisa
    # saca estadisticos utiles para Sepectral sumary
    # crea el espectral sumary

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
    header["template"] = data_in[4][2]
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

    return fisa  # SpectralSumary(fisa)


# def read_starlight(path, **):
# leer al archivo en formato starlight
# saca estadisticos utiles para Sepectral sumary
# crea el espectral sumary

#   return SpectralSumary(....)
