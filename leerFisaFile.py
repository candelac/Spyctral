import os

mainpath = "/CursoInformaticaCientifica/Spyctral"
filename = "case_SC_FISA.fisa"
fullpath = os.path.join(mainpath, filename)

# Función que lee un archivo .fisa y obtiene 4 tablas correspondientes a:
# Unreddened Spectrum, Template Spectrum, Observed Spectrum y Residual Flux.
# También obtiene los valores de:
# Reddening y Normalization Point.
# Uso:
#      [unreddened, template, observed, residual_flux,reddening,
#           normalization_point] = read_fisa(fullpath)


def read_fisa(fullpath):
    nombre, extension = os.path.splitext(fullpath)
    if extension != ".fisa":  # verificar que sea un archivo correcto
        print("Formato incorrecto de archivo debe tener extensión .fisa")
        return 1
    with open(fullpath) as archivo:
        unreddened = list()
        template = list()
        observed = list()
        residual_flux = list()

        if not archivo.readable():
            print("Archivo no se puede leer, verificar permisos.")

        linea = archivo.readline()
        fields = linea.strip().split()
        clasifile = 0

        while linea != "":
            # lectura de Reddening y Normalization Point
            if linea.startswith(" # Reddening:"):
                reddening = fields[-1]
            if linea.startswith(" # Normalization Point:"):
                normalization_point = fields[-1]

            linea = archivo.readline()   # Carga en cada ciclo while
            fields = linea.strip().split()

            # Detección y lectura de Unreddened Spectrum
            if linea.startswith(" #"):
                continue
            if (len(fields) > 1) & (clasifile == 0):
                fields = [float(dato) for dato in fields]
                unreddened.append(fields)

            # Detección y lectura de Template Spectrum
            if (linea.startswith("\n")):
                linea = archivo.readline()
                if (linea.startswith("\n")):
                    clasifile += 1
            if (len(fields) > 1) & (clasifile == 1):
                fields = [float(dato) for dato in fields]
                template.append(fields)

            # Detección y lectura de Observed Spectrum
            if (linea.startswith("\n")):
                linea = archivo.readline()
                if (linea.startswith("\n")):
                    clasifile += 1
            if (len(fields) > 1) & (clasifile == 2):
                fields = [float(dato) for dato in fields]
                observed.append(fields)

            # Detección y lectura de Residual Flux
            if (linea.startswith("\n")):
                linea = archivo.readline()
                if (linea.startswith("\n")):
                    clasifile += 1
            if (len(fields) > 1) & (clasifile == 3):
                fields = [float(dato) for dato in fields]
                residual_flux.append(fields)
    return unreddened, template, observed, residual_flux, reddening, \
        normalization_point


[unreddened, template, observed, residual_flux,
    reddening, normalization_point] = read_fisa(fullpath)
