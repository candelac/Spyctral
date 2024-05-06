# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import attrs

from .utils.bunch import Bunch

# Esta clase habría que re diseñarla/sacarla

@attrs.define
class SpectralSummary:
    header = attrs.field(converter=lambda v: Bunch("header_items:", v))
    data = attrs.field(converter=lambda v: Bunch("data_items:", v))

'''
# -----------------------------------------------------------------------------
# clases adaptadas de feets:

# =============================================================================
# IMPORTS
# =============================================================================

import copy
import itertools as it
from collections import Counter
from collections.abc import Mapping

import attr

import numpy as np

from . import extractors
from .extractors.core import (
    DATAS,
    DATA_FISA,  # esto preguntar a marti
    DATA_STL,
)

# =============================================================================
# EXCEPTIONS
# =============================================================================


class FeatureNotFound(ValueError):
    """Raises when a non-available feature are requested.

    A non-available feature can be:

    - The feature don't exist in any of the registered extractor.
    - The feature can't be requested with the available data.

    """


class DataRequiredError(ValueError):
    """Raised when the feature-space required another data."""


class FeatureSpaceError(ValueError):
    """The FeatureSpace can't be configured with the given parameters."""


# =============================================================================
# RESULTSET
# =============================================================================


class _Map(Mapping):
    """Internal representation of a immutable dict"""

    def __init__(self, d):
        self._keys = tuple(d.keys())
        self._values = tuple(d.values())

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y]"""
        if k not in self._keys:
            raise KeyError(k)
        idx = self._keys.index(k)
        return self._values[idx]

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return iter(self._keys)

    def __len__(self):
        """x.__len__() <==> len(x)"""
        return len(self._keys)


@attr.s(frozen=True, auto_attribs=True, repr=False)
class FeatureSet:
    """Clase que va a contener/mostrar los features"""

    features_names: tuple = attr.ib(converter=tuple)
    values: dict = attr.ib(converter=_Map)
    extractors: dict = attr.ib(converter=_Map)
    timeserie: dict = attr.ib(converter=_Map)

    def __attrs_post_init__(self):
        cnt = Counter(
            it.chain(self.features_names, self.values, self.extractors)
        )
        diff = set(k for k, v in cnt.items() if v < 3)
        if diff:
            joined_diff = ", ".join(diff)
            raise FeatureNotFound(
                f"The features '{joined_diff}' must be in 'features_names' "
                "'values' and 'extractors'"
            )

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return iter(self.as_arrays())

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y]"""
        return copy.deepcopy(self.values[k])

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        feats = ", ".join(self.features_names)
        ts = ", ".join(d for d in DATAS if self.timeserie.get(d) is not None)
        return f"FeatureSet(features=<{feats}>, timeserie=<{ts}>)"

    def extractor_of(self, feature):
        """Retrieve the  extractor instance used for create the feature."""
        return copy.deepcopy(self.extractors[feature])

    # def plot(self): ...

    # def as_arrays(self): ...

    def as_dict(self):
        """Return a copy of values"""
        return dict(self.values)

    # def as_dataframe(self): ...


# =============================================================================
# FEATURE EXTRACTORS
# =============================================================================


class FeatureSpace:
    """Clase que permite seleccionar los features (edad, enrojecimiento,
    metalicidad, etc) que se pueden calcular basado en los datos que se tienen
    disponibles (fisa, starlight).
    Los features que da son los que satisfacen todos los filtros.

    Parameters
    ----------

    data : array-like, optional, default ``None``
        fisa o starlight

    only : array-like, optional, default ``None``
        features que queres calcular, ej: edad, metalicidad

    exclude : array-like, optional, default ``None``
        features que no queres calcular

    kwargs : `Feature_name={param1: value, param2: value, ...}``
        parámetros extra para configurar los extractors
    """

    def __init__(self, data=None, only=None, exclude=None, **kwargs):
        # retrieve all the extractors
        exts = extractors.registered_extractors()

        # store all the parameters for the extractors
        self._kwargs = kwargs

        # get all posible features by data (segun sea None o dado)
        if data:
            fbdata = []
            for fname, f in exts.items():
                if not f.get_required_data().difference(data):
                    fbdata.append(fname)
        else:
            fbdata = exts.keys()
        self._data = frozenset(data or extractors.DATAS)
        self._features_by_data = frozenset(fbdata)

        # validate the list of features or select all of them
        if only:
            for f in only:
                if f not in exts:
                    raise FeatureNotFound(f)
        self._only = frozenset(only or exts.keys())

        # select the features to exclude or not exclude anything
        if exclude:
            for f in exclude:
                if f not in exts:
                    raise FeatureNotFound(f)
        self._exclude = frozenset(exclude or ())

        # the candidate to be the features to be extracted:
        # features entre data y only, menos los exclude
        candidates = self._features_by_data.intersection(
            self._only
        ).difference(self._exclude)

        # remove by dependencies
        if only or exclude:
            final = set()
            for f in candidates:
                fcls = exts[f]
                dependencies = fcls.get_dependencies()
                if dependencies.issubset(candidates):
                    final.add(f)
        else:
            final = candidates

        # the final features
        self._features = frozenset(final)

        # create a ndarray for all the results (ordenado)
        self._features_as_array = np.array(sorted(self._features))

        # initialize the extractors and determine the required data only
        features_extractors, features_extractors_names = set(), set()
        required_data = set()
        for fcls in set(exts.values()):  # exts=extractores
            if fcls.get_features().intersection(self._features):
                # if: solo los features que necesito sg data

                params = self._kwargs.get(fcls.__name__, {})
                fext = fcls(**params)

                features_extractors.add(fext)
                features_extractors_names.add(fext.name)
                required_data.update(fext.get_required_data())

        if not features_extractors:
            raise FeatureSpaceError("No feature extractor was selected")

        self._features_extractors = frozenset(features_extractors)
        self._features_extractors_names = frozenset(features_extractors_names)
        self._required_data = frozenset(required_data)

        # excecution order by dependencies
        # sort_by_dependencies: calcula el orden de resolución de los extractor
        self._execution_plan = extractors.sort_by_dependencies(
            features_extractors
        )

        not_found = set(self._kwargs).difference(
            self._features_extractors_names
        )
        if not_found:
            joined_not_found = ", ".join(not_found)
            raise FeatureNotFound(
                "This space not found feature(s) extractor(s) "
                f"{joined_not_found} to assign the given parameter(s)"
            )

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return str(self)

    def __str__(self):
        """x.__str__() <==> str(x)"""
        if not hasattr(self, "__str"):
            extractors = [str(extractor) for extractor in self._execution_plan]
            space = ", ".join(extractors)
            self.__str = "<FeatureSpace: {}>".format(space)
        return self.__str

    def preprocess_timeserie(self, d):  # esto es necesario?
        """Validate if the required values of the time-serie exist with
        non ``None`` values in the dict ``d``. Finally returns a
        new dictionary whose non-null values have been converted to
        ``np.ndarray``
        """
        array_data = {}
        for k, v in d.items():
            if k in self._required_data and v is None:
                raise DataRequiredError(k)
            array_data[k] = v if v is None else np.asarray(v)
        return array_data

    def extract(
        self,
        fisa=None,
        starlight=None,
    ):
        """Extrae los features de fisa o starlight.
        This method must be provided with the required timeseries data
        specified in the attribute ``required_data_``.

        Parameters
        ----------
        fisa : iterable, optional
        starlight : iterable, optional

        Returns
        -------
        spyctral.core.FeatureSet
            Container of a calculated features.

        """
        timeserie = self.preprocess_timeserie(  # ver
            {
                DATA_FISA: fisa,
                DATA_STL: starlight,
            }
        )

        # ejecuta los extractors:
        features, extractors = {}, {}
        for fextractor in self._execution_plan:
            # .extract de la clase Extractor: extrae los parametros necesarios
            # para ejecutar la extracción del feature y lo ejecuta
            result = fextractor.extract(features=features, **timeserie)
            for fname, fvalue in result.items():
                features[fname] = fvalue
                extractors[fname] = copy.deepcopy(fextractor)

        # remove all the not needed features and extractors
        flt_features, flt_extractors = {}, {}
        for fname in self._features_as_array:
            flt_features[fname] = features[fname]
            flt_extractors[fname] = extractors[fname]

        rs = FeatureSet(
            features_names=self._features_as_array,
            values=flt_features,
            extractors=flt_extractors,
            timeserie=timeserie,
        )
        return rs

    @property
    def extractors_conf(self):
        return copy.deepcopy(self._kwargs)

    @property
    def data(self):
        return self._data

    @property
    def only(self):
        return self._only

    @property
    def exclude(self):
        return self._exclude

    @property
    def features_by_data_(self):
        return self._features_by_data

    @property
    def features_(self):
        return self._features

    @property
    def features_extractors_(self):
        return self._features_extractors

    @property
    def features_as_array_(self):
        return self._features_as_array

    @property
    def excecution_plan_(self):
        return self._execution_plan

    @property
    def required_data_(self):
        return self._required_data
'''