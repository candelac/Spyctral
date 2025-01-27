# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# This code was ripped of from scikit-criteria on 07-nov-2023.
# https://github.com/quatrope/scikit-criteria/blob/ec63c/skcriteria/utils/bunch.py
# Util this point the copyright is
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2016-2021, Cabral, Juan; Luczywo, Nadia
# Copyright (c) 2022, QuatroPe
# All rights reserved.


# =============================================================================
# DOCS
# =============================================================================

"""Container object exposing keys as attributes."""


# =============================================================================
# IMPORTS
# =============================================================================

import copy
from collections.abc import Mapping


# =============================================================================
# DOC INHERITANCE
# =============================================================================


class Bunch(Mapping):
    """
    Descripción en castellano:
    Clase que actúa como un contenedor para datos, permitiendo el acceso a sus
    elementos tanto mediante claves como si fueran atributos.
    La clase Bunch tiene el propósito de organizar y manejar de manera eficiente los
    datos encapsulados en las diferentes propiedades del objeto SpectralSummary.
    Proporciona una estructura flexible que permite acceder a los datos de dos formas
    diferentes: como un diccionario (clave-valor) y como atributos (objeto.propiedad).
    Esto facilita la manipulación de datos en código que podría volverse más complejo
    si se utilizara un formato de solo diccionario.

    Propósito:
    Esta clase es útil para organizar y acceder a datos de forma más intuitiva,
    ya que combina las funcionalidades de un diccionario y un objeto de Python.

    Atributos:
        _name (str): Nombre descriptivo del objeto `Bunch`.
        _data (dict-like): Diccionario que almacena los datos.

    Ejemplo de uso:
    >>> b = Bunch("data", {"a": 1, "b": 2})
    >>> b.a  # Acceso como atributo
    1
    >>> b["b"]  # Acceso como clave
    2

    *************************************************************************************
    *************************************************************************************
    Description in English:
    Class that acts as a container for data, allowing access to its elements
    both by keys and as if they were attributes.
    The Bunch class is designed to efficiently organize and manage the data encapsulated
    in the various properties of the SpectralSummary object. It provides a flexible
    structure that allows data to be accessed in two different ways: as a dictionary
    (key-value) and as attributes (object.property). This dual access approach simplifies
    data manipulation in code that could otherwise become more complex if only a
    dictionary format were used.

    Purpose:
    This class is useful for organizing and accessing data more intuitively,
    as it combines the functionalities of a dictionary and a Python object.

    Attributes:
        _name (str): Descriptive name of the `Bunch` object.
        _data (dict-like): Dictionary storing the data.

    Example usage:
    >>> b = Bunch("data", {"a": 1, "b": 2})
    >>> b.a  # Access as an attribute
    1
    >>> b["b"]  # Access as a key
    2
    """

    def __init__(self, name, data):
        """
        Descripción en castellano:
        Constructor de la clase Bunch. Inicializa un nuevo objeto `Bunch` con un nombre
        y un conjunto de datos.

        Argumentos:
            name (str): Nombre descriptivo del objeto Bunch.
            data (dict-like): Diccionario que contiene los datos a almacenar.

        Propósito:
        Este método establece los atributos internos `_name` y `_data`, donde `_name` es
        una etiqueta descriptiva y `_data` almacena los datos proporcionados en un
        diccionario o estructura similar.

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Constructor of the Bunch class. Initializes a new `Bunch` object with a name and
        a set of data.

        Arguments:
            name (str): Descriptive name of the Bunch object.
            data (dict-like): Dictionary containing the data to be stored.

        Purpose:
        This method sets the internal attributes `_name` and `_data`, where `_name`
        is a descriptive label and `_data` stores the provided data in a dictionary or
        similar structure.
        """
        self._name = str(name)
        self._data = data

    def __getitem__(self, k):
        """
        Descripción en castellano:
        Permite acceder a los elementos almacenados en `_data` utilizando la sintaxis de
        indexación.

        Argumentos:
            k (str): Clave del elemento a recuperar.

        Retorna:
            Cualquier tipo: Valor asociado a la clave proporcionada en `_data`.

        Propósito:
            Este método habilita la indexación como en un diccionario estándar, es decir,
            permite recuperar valores mediante `objeto[k]`, donde `objeto` es una
            instancia de `Bunch`.

        Ejemplo:
            >>> b = Bunch("example", {"a": 1, "b": 2})
            >>> b["a"]
            1

            x.__getitem__(y) <==> x[y].

        *************************************************************************************
        *************************************************************************************
        Description in English:
        Allows accessing elements stored in `_data` using indexing syntax.

        Arguments:
            k (str): Key of the element to retrieve.

        Returns:
            Any type: Value associated with the provided key in `_data`.

        Purpose:
        This method enables dictionary-like indexing, allowing values to be retrieved
        using `object[k]`, where `object` is an instance of `Bunch`.

        Example:
            >>> b = Bunch("example", {"a": 1, "b": 2})
            >>> b["a"]
            1
            x.__getitem__(y) <==> x[y].
        """
        return self._data[k]

    def __getattr__(self, a):
        """x.__getattr__(y) <==> x.y."""
        try:
            return self._data[a]
        except KeyError:
            raise AttributeError(a)

    def __copy__(self):
        """x.__copy__() <==> copy.copy(x)."""
        cls = type(self)
        return cls(str(self._name), data=self._data)

    def __deepcopy__(self, memo):
        """x.__deepcopy__() <==> copy.copy(x)."""
        # extract the class
        cls = type(self)

        # make the copy but without the data
        clone = cls(name=str(self._name), data=None)

        # store in the memo that clone is copy of self
        # https://docs.python.org/3/library/copy.html
        memo[id(self)] = clone

        # now we copy the data
        clone._data = copy.deepcopy(self._data, memo)

        return clone

    def __iter__(self):
        """x.__iter__() <==> iter(x)."""
        return iter(self._data)

    def __len__(self):
        """x.__len__() <==> len(x)."""
        return len(self._data)

    def __repr__(self):
        """x.__repr__() <==> repr(x)."""
        """
        Descripción en castellano:
        Devuelve una representación en forma de cadena de texto de la instancia de la
        clase `Bunch`.
        Muestra el nombre de la instancia y las claves almacenadas en el diccionario
        `_data` en un formato legible.

        Retorna:
            str: Una representación en texto del objeto, indicando su nombre y las claves
            contenidas en `_data`.

        Propósito:
        Este método facilita la depuración y visualización de objetos `Bunch`, mostrando
        información clave en un formato legible.

        Ejemplo:
        >>> b = Bunch("example", {"a": 1, "b": 2})
        >>> repr(b)
        '<example {'a', 'b'}>'

        *********************************************************************************
        *********************************************************************************
        Description in English:
        Returns a string representation of the `Bunch` class instance.
        It shows the instance name and the keys stored in the `_data` dictionary in a
        readable format.

        Returns:
            str: A textual representation of the object, displaying its name and the keys
            contained in `_data`.

        Purpose:
            This method facilitates debugging and visualization of `Bunch` objects by
            resenting key information in a readable format.

        Example:
        >>> b = Bunch("example", {"a": 1, "b": 2})
        >>> repr(b)
        '<example {'a', 'b'}>'
        """
        content = repr(set(self._data)) if self._data else "{}"
        return f"<{self._name} {content}>"

    def __dir__(self):
        """x.__dir__() <==> dir(x)."""
        return super().__dir__() + list(self._data)
