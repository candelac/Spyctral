# Importamos los paquetes que necesitamos
import os


# Creamos la clase que define el objeto base
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

    # Aquí leo el archivo tipo FISA

    def read_fisa(lines):
        pass
