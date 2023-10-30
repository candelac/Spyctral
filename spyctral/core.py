import attrs

from .utils.bunch import Bunch


@attrs.define
class SpectralSummary:
    data_in = attrs.field()
    header = attrs.field(converter=lambda v: Bunch("header", v))
