import os
import re
import astropy.units as u
from astropy.table import QTable

class SpectralSummary:
    def __init__(self):
        self.version = None
        self.date = None
        self.time = None
        self.Reddening = None
        self.original_file = None
        self.Normalization_point = None
        self.unreddened_spec = None
        self.template_spec = None
        self.observed_spec = None
        self.residual_spec = None

def read_fisa(path):
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
    ss_object = SpectralSummary()
    file = open(path, "r")
    data_in = [k for k in file.read().splitlines()]
    file.close()
    Unreddened_spectrum = []
    Template_spectrum = []
    Observed_spectrum = []
    Residual_flux = []
    index_counter = 0
    for line in data_in:
        if re.search(r' #', line) is not None:
            # FISA Version extraction
            if re.search(r'FISA v.', line) is not None:
                ss_object.version = float(re.search('\d+\.\d+', line)[0])
            # Date extraction 
            if re.search(r'Date', line) is not None:
                ss_object.date = re.search(r'(\d+/\d+/\d+)', line)[0]
            # Time extraction 
            if re.search(r'time', line) is not None:
                ss_object.time = re.search(r'(\d+:\d+:\d+)', line)[0]
            # Reddening value extraction
            if re.search(r'Reddening', line) is not None:
                ss_object.Reddening = float(re.search('\d+\.\d+', line)[0])
            # File extraction 
            if re.search(r'Templated', line) is not None:
                ss_object.original_file = re.search(r'\w+.dat$', line)[0]
            # Normalization point extraction 
            if (re.search(r'Normalization Point', line)) is not None:
                ss_object.Normalization_point = float(re.search('\d+\.\d+', line)[0])

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
            

    ss_object.unreddened_spec = QTable(rows=Unreddened_spectrum, names=['Wave_length', 'values'])
    ss_object.template_spec = QTable(rows=Template_spectrum, names=['Wave_length', 'values'])
    ss_object.observed_spec = QTable(rows=Observed_spectrum, names=['Wave_length', 'values'])
    ss_object.residual_spec = QTable(rows=Residual_flux, names=['Wave_length', 'values'])

    return ss_object

path = 'Add_on/case_SC_FISA.fisa' # path for testig the function

abc = read_fisa(path)

print(f'La version de FISA utilizada es: V.{abc.version}\n El archivo utilizad: {abc.original_file}\n El Reddening point {abc.Reddening}\n El Normalizatio point es de: {abc.Normalization_point}')
print(f'Unredended table\n {abc.unreddened_spec}')