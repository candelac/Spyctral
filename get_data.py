import pandas as pd
import re

# path = 'Add_on/case_SC_FISA.fisa' # path for testig the function
def get_fisa_data(path: str):
    """ This function takes as input the path of the FISA file reads it and
    returns four dataframes"""
    f = open(path, 'r')
    Unreddened_spectrum = list()
    Template_spectrum = list()
    Observed_spectrum = list()
    Residual_flux = list()
    index_counter = 0
    for line in f.readlines():
        if re.search(r' #', line) is None:
            values = str(line).strip().replace('\n', '').strip().split('    ')
            if ((len(values) > 1) & (index_counter < 1) ): # Salta los dos primeros espacios en blanco
                values = [float(x) for x in values]
                Unreddened_spectrum.append(values)
            elif ((len(values) > 1) & (index_counter < 2) & (index_counter >= 1)):  # Salta los segundos dos espacios en blanco
                values = [float(x) for x in values]
                Template_spectrum.append(values)
            elif ((len(values) > 1) & (index_counter < 3) & (index_counter >= 2)):  # salta los terceros dos espacios en blanco
                values = [float(x) for x in values]
                Observed_spectrum.append(values)
            elif ((len(values) > 1) & (index_counter < 4) & (index_counter >= 3)): 
                values = [float(x) for x in values]
                Residual_flux.append(values)
            else:
                index_counter = index_counter + 0.5
            

    Unreddened_spectrum = pd.DataFrame(Unreddened_spectrum, columns=['wave_len', 'values'])
    Template_spectrum = pd.DataFrame(Template_spectrum, columns=['wave_len', 'values'])
    Observed_spectrum = pd.DataFrame(Observed_spectrum, columns=['wave_len', 'values'])
    Residual_flux = pd.DataFrame(Residual_flux, columns=['wave_len', 'values'])
    
    return Unreddened_spectrum, Template_spectrum, Observed_spectrum, Residual_flux



def get_Reddening_fisa(path: str):
    """ This function takes the path of the FISA file and returns
    the Reddenging value"""
    f = open(path, 'r')
    for line in f.readlines():
        if (re.search(r'Reddening', line)) is not None:
            Reddening = re.search('\d+\.\d+', line)[0]
        else:
            Reddening = None

    return Reddening


def get_NormPoint_fisa(path: str):
    """ This function takes the path of the FISA file and returns
    the Normalization point value"""
    f = open(path, 'r')
    for line in f.readlines():
        if (re.search(r'Normalization Point', line)) is not None:
            Normalization_point = re.search('\d+\.\d+', line)[0]
        else:
            Normalization_point = None

        return Normalization_point