import os
import astropy.units as u
from astropy.table import QTable
import re

#path = 'Add_on/case_SC_FISA.fisa' # path for testig the function
def get_fisa_data(path: str):
    """
    Función que lee archivo FISA.

    Parameters
    ----------
    path : "str"
        Name of file

    Return
    ----------
    fisa : dict

    """
    assert os.path.exists(path),"File not found"

    file = open(path, "r")
    data_in = [k for k in file.read().splitlines()]
    file.close()
    Version = None
    Date = None
    Time = None
    original_File = None
    Reddening = None
    Version = None
    Unreddened_spectrum = []
    Template_spectrum = []
    Observed_spectrum = []
    Residual_flux = []
    index_counter = 0
    for line in data_in:
        if re.search(r' #', line) is not None:
            # FISA Version extraction
            if re.search(r'FISA v.', line) is not None:
                Version = float(re.search('\d+\.\d+', line)[0])
            # Date extraction 
            if re.search(r'Date', line) is not None:
                Date = re.search(r'(\d+/\d+/\d+)', line)[0]
            # Time extraction 
            if re.search(r'time', line) is not None:
                Time = re.search(r'(\d+:\d+:\d+)', line)[0]
            # Reddening value extraction
            if re.search(r'Reddening', line) is not None:
                Reddening = float(re.search('\d+\.\d+', line)[0])
            # File extraction 
            if re.search(r'Templated', line) is not None:
                original_File = re.search(r'\w+.dat$', line)[0]
            # Normalization point extraction 
            if (re.search(r'Normalization Point', line)) is not None:
                Normalization_point = float(re.search('\d+\.\d+', line)[0])

        if re.search(r' #', line) is None:
            values = line.split()
            if len(values) > 1 and index_counter < 1:  # Salta los dos primeros espacios en blanco
                values = [float(x) for x in values]
                Unreddened_spectrum.append(values)
            elif len(values) > 1 and index_counter < 2 and index_counter >= 1:  # Salta los segundos dos espacios en blanco
                values = [float(x) for x in values]
                Template_spectrum.append(values)
            elif len(values) > 1 and index_counter < 3 and index_counter >= 2:  # salta los terceros dos espacios en blanco
                values = [float(x) for x in values]
                Observed_spectrum.append(values)
            elif len(values) > 1 and index_counter < 4 and index_counter >= 3: 
                values = [float(x) for x in values]
                Residual_flux.append(values)
            else:
                index_counter = index_counter + 0.5
            

    Unreddened_spectrum = QTable(rows=Unreddened_spectrum, names=['Wave_length', 'values'])
    Template_spectrum = QTable(rows=Template_spectrum, names=['Wave_length', 'values'])
    Observed_spectrum = QTable(rows=Observed_spectrum, names=['Wave_length', 'values'])
    Residual_flux = QTable(rows=Residual_flux, names=['Wave_length', 'values'])

    return Unreddened_spectrum, Template_spectrum, Observed_spectrum, Residual_flux


