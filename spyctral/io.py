import re

import dateutil.parser

import numpy as np

from . import core


FISA_RX_SPECTRA_NAMES = re.compile(r"Index (?P<index>\d) = (?P<value>[^\n]+)")

FISA_RX_DATE_AND_TIME = re.compile(
    r"Date (?P<date>\d{2}/\d{2}/\d{4}); time (?P<time>\d{2}:\d{2}:\d{2})"
)

FISA_RX_REDDENING = re.compile(r"Reddening:\s+(?P<value>[\d.][^\n]+)")

FISA_RX_TEMPLATE = re.compile(r"Adopted Templated:\s*(?P<ruta>[\S]+)")

FISA_RX_NORMALIZATION_POINT = re.compile(
    r"Normalization Point:\s+(?P<value>[\d.][^\n]+)"
)

FISA_RX_VERSION = re.compile(
    r"SPECTRUM ANALYZED WITH FISA v\.\s+(?P<value>[\d.][^\n]+)"
)


def _process_header(lines):
    src = "\n".join(lines)

    fisa_version = FISA_RX_VERSION.findall(src)[0]

    date, time = FISA_RX_DATE_AND_TIME.findall(src)[0]
    datetime = dateutil.parser.parse(f"{date} {time}")

    reddening = float(FISA_RX_REDDENING.findall(src)[0])
    adopted_templated = FISA_RX_TEMPLATE.findall(src)[0]
    normalization_point = float(FISA_RX_NORMALIZATION_POINT.findall(src)[0])

    names = {}
    for match in FISA_RX_SPECTRA_NAMES.finditer(src):
        idx = int(match.group("index"))
        name = match.group("value")
        names[idx] = name
    names = tuple(name for _, name in sorted(names.items()))

    header = {
        "fisa_version": fisa_version,
        "dateime": datetime,
        "reddening": reddening,
        "adopted_templated": adopted_templated,
        "normalization_point": normalization_point,
        "names": names,
    }

    return header


def read_fisa(path_or_buffer):
    header_lines, spectras_lines = [], []
    current_spectra = []
    with open(path_or_buffer, "r") as fp:
        for line in fp:
            if line.startswith(" #"):
                header_lines.append(line.strip())
            elif line.strip():
                lamb, flux = map(float, line.split())
                current_spectra.append([lamb, flux])
            elif current_spectra and not line.strip():
                spectras_lines.append(np.array(current_spectra, dtype=float))
                current_spectra = []

    if current_spectra:
        spectras_lines.append(np.array(current_spectra, dtype=float))
        del current_spectra

    header = _process_header(header_lines)

    return core.SpectralSummary(None, extra=header)
