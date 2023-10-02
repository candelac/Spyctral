import pandas as pd
import re


def get_fisa_data(Path):
    f = open('Add_on/case_SC_FISA.fisa' , 'r')
    Unreddened_spectrum = list()
    Template_spectrum = list()
    Observed_spectrum = list()
    Residual_flux = list()
    for line in f.readlines():
        if (re.search(r'Reddening', line)) is not None:
            Reddening = re.search('\d+\.\d+',line)[0]
        if (re.search(r'Normalization Point', line)) is not None:
            Normalization_point = re.search('\d+\.\d+',line)[0]
        if re.search(r' #', line) is None:
            values = str(line).strip().replace('\n' , '').split('.')

            if (len(values) > 2): # este if elimina las lineas en blanco
                Unreddened_spectrum.append(int(values[0]))
                ts , os = values[1].split(' ' , 1)
                Template_spectrum.append(int(ts))
                Observed_spectrum.append(int(os))
                Residual_flux.append(float(values[2].replace("E" , 'e')))

    data = pd.DataFrame([Unreddened_spectrum, Template_spectrum,
                          Observed_spectrum, Residual_flux], index=
                          ['Unreddened_spectrum', 'Template_spectrum',
                            'Observed_spectrum', 'Residual_flux']).T
    return data


def get_Reddening_fisa(path):
    f = open('Add_on/case_SC_FISA.fisa', 'r')
    for line in f.readlines():
        if (re.search(r'Reddening', line)) is not None:
            Reddening = re.search('\d+\.\d+', line)[0]
        else:
            Reddening = None

    return Reddening


def get_NormPoint_fisa(path):
    f = open('Add_on/case_SC_FISA.fisa', 'r')
    for line in f.readlines():
        if (re.search(r'Normalization Point', line)) is not None:
            Normalization_point = re.search('\d+\.\d+', line)[0]
        else:
            Normalization_point = None

        return Normalization_point