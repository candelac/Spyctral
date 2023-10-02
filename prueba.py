import numpy as np 
import pandas as pd 
import os 

#Creamos la clase que define el objeto base
class SpectralSummary():

    def __init__(self, filepath):
        """ This is the constructor that lets us create
        objects from this class.

        Parameters
        ----------
        filepath: string
            file path of the starlight output

        Returns
        -------


        """
        # Verificamos si existe el archivo
        assert (os.path.exists(filepath)), f'This file ({filepath}) does not exist. Please check it.'

        # Leemos el archivo 
        file = open(filepath, 'r')
        nombre_archivo, extension = os.path.splitext(filepath)
        lines = file.readlines()

        if extension == '.fisa':
            self.fisa = read_fisa(file)
        elif extension == '.out':
            self.starlight = read_starlight(file)

        file.close()
