import attrs

from .utils.bunch import Bunch



@attrs.define
class SpectralSummary:
    data_in = attrs.field()
    extra = attrs.field(converter=lambda v: Bunch("extra", v))
