# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.


# Copiado de feets, y comentado lo que creo que hace cada funcion #


# =============================================================================
# DOCS
# =============================================================================

"""Features extractors classes and register utilities"""

__all__ = [
    "DATAS",
    "register_extractor",
    "registered_extractors",
    "is_registered",
    "available_features",
    "extractor_of",
    "sort_by_dependencies",
    "ExtractorBadDefinedError",
    "ExtractorContractError",
    "ExtractorWarning",
    "Extractor",
    "AgeFisa",
    "AgeStl",
]

# =============================================================================
# IMPORTS
# =============================================================================

import inspect

from .core import (
    DATAS,
    Extractor,
    ExtractorBadDefinedError,
    ExtractorContractError,
    ExtractorWarning,
)
from .ext_fisa_age import AgeFisa  # movido de la linea 154
from .ext_stl_age import AgeStl


# =============================================================================
# REGISTER UTILITY
# =============================================================================

_extractors = {}

# "Registra una determinada clase Extractor en la infraestructura de feets."

# Esta funcion se fija que la clase tipo Extractor esta bien definida ?


def register_extractor(cls):
    """Register a given extractor class into the feets insfrastructure."""
    if not inspect.isclass(cls) or not issubclass(cls, Extractor):
        msg = "'cls' must be a subclass of Extractor. Found: {}"
        raise TypeError(msg.format(cls))
    for d in cls.get_dependencies():
        if d not in _extractors.keys():
            msg = "Dependency '{}' from extractor {}".format(d, cls)
            raise ExtractorBadDefinedError(msg)

    _extractors.update((f, cls) for f in cls.get_features())
    return cls


# Esta funcion retorna un diccionario con todos los extractores disponibles
# las 'keys' son las caracteristicas a determinar por el extractor (value)


def registered_extractors():
    """Returns all the available extractor classes as a dicctionries where
    the key is the feature extracted for the extractor on the *value*.

    Notes
    -----
    Multiple features can be extracted with the same extractor

    """
    return dict(_extractors)


# Comprueba si el Extractor ya está registrado.


def is_registered(obj):
    """Check if a given extractor class is already registered."""
    if isinstance(obj, str):
        features = [obj]
    elif not inspect.isclass(obj) or not issubclass(obj, Extractor):
        msg = "'cls' must be a subclass of Extractor. Found: {}"
        raise TypeError(msg.format(obj))
    else:
        features = obj.get_features()
    return {f: (f in _extractors) for f in features}


# Retorna todas las caracteristicas disponibles,
# las saca del diccionario que hizo antes en registered_extractors()


def available_features():
    """Retrieve all the current available features in feets."""
    return sorted(_extractors.keys())


# Para una dada característica que se quiere calcular,
# esta funcion retorna el extractor registrado para hacerlo


def extractor_of(feature):
    """Retrieve the current register extractor class for the given feature."""
    return _extractors[feature]


# Esta funcion es llamada en FeatureSpace para determinar el orden
# de resolución de los extractores de características


def sort_by_dependencies(exts, retry=None):
    """Calculate the Feature Extractor Resolution Order."""
    sorted_ext, features_from_sorted = [], set()
    pending = [(e, 0) for e in exts]
    retry = len(exts) * 100 if retry is None else retry
    while pending:
        ext, cnt = pending.pop(0)

        if not isinstance(ext, Extractor) and not issubclass(ext, Extractor):
            msg = "Only Extractor instances are allowed. Found {}."
            raise TypeError(msg.format(type(ext)))

        deps = ext.get_dependencies()
        if deps.difference(features_from_sorted):
            if cnt + 1 > retry:
                msg = "Maximun retry ({}) to sort achieved from extractor {}."
                raise RuntimeError(msg.format(retry, type(ext)))
            pending.append((ext, cnt + 1))
        else:
            sorted_ext.append(ext)
            features_from_sorted.update(ext.get_features())
    return tuple(sorted_ext)


# =============================================================================
# REGISTERS
# =============================================================================

# Aquí importamos los ext_caracteristica.py que estan en la carpeta extractors

# from .ext_fisa_age import *
# from .ext_stl_age import *


# Aqui se itera sobre las subclases de Extractor,
# después de haberlas ordenado por dependencias
# y luego registra cada una de esas clases

for cls in sort_by_dependencies(Extractor.__subclasses__()):
    register_extractor(cls)

del cls
