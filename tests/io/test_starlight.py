# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

"""STARLIGHT test input data."""

# =============================================================================
# IMPORTS
# =============================================================================

import datetime as dt


from astropy.table import QTable

import numpy as np

import pandas as pd

# import pytest

from specutils import Spectrum1D

from spyctral.core import core
from spyctral.io import starlight
from spyctral.utils.bunch import Bunch


# =============================================================================
# STARLIGHT TESTS
# =============================================================================


def test_read_starlight(file_path):
    path = file_path("case_SC_Starlight.out")

    summary = starlight.read_starlight(path)

    assert isinstance(summary, core.SpectralSummary)

    assert isinstance(summary.header, Bunch)
    assert isinstance(summary.header.Date, dt.datetime)
    # assert isinstance(summary.header.Cid@UFSC, ? ) # ?
    assert isinstance(summary.header.arq_obs, str)
    assert isinstance(summary.header.arq_base, str)
    assert isinstance(summary.header.arq_masks, str)
    assert isinstance(summary.header.arq_config, str)
    assert isinstance(summary.header.N_base, float)
    assert isinstance(summary.header.N_YAV_components, float)
    assert isinstance(summary.header.i_FitPowerLaw, float)
    assert isinstance(summary.header.alpha_PowerLaw, float)
    assert isinstance(summary.header.red_law_option, str)
    assert isinstance(summary.header.q_norm, float)
    assert isinstance(summary.header.l_ini, float)
    assert isinstance(summary.header.l_fin, float)
    assert isinstance(summary.header.dl, float)
    assert isinstance(summary.header.l_norm, float)
    assert isinstance(summary.header.llow_norm, float)
    assert isinstance(summary.header.lupp_norm, float)
    assert isinstance(summary.header.fobs_norm, float)
    assert isinstance(summary.header.llow_SN, float)
    assert isinstance(summary.header.lupp_SN, float)
    assert isinstance(summary.header.S_N_in_S_N_window, float)
    assert isinstance(summary.header.S_N_in_norm_window, float)
    assert isinstance(summary.header.S_N_err_in_S_N_window, float)
    assert isinstance(summary.header.S_N_err_in_norm_window, float)
    assert isinstance(summary.header.fscale_chi2, float)
    assert isinstance(summary.header.idum_orig, float)
    assert isinstance(summary.header.NOl_eff, float)
    assert isinstance(summary.header.Nl_eff, float)
    assert isinstance(summary.header.Ntot_cliped, float)
    assert isinstance(summary.header.clip_method, str)
    assert isinstance(summary.header.N_chains, float)
    assert isinstance(summary.header.NEX0s_base, float)
    # assert isinstance(summary.header.Clip-Bug, float) # lee mal el -
    # assert isinstance(summary.header.RC-Crash, float) # lee mal el -
    # assert isinstance(summary.header.Burn-Inwarning-flags, float) # lee mal
    assert isinstance(summary.header.n_censored_weights, float)
    assert isinstance(summary.header.wei_nsig_threshold, float)
    assert isinstance(summary.header.wei_limit, float)
    assert isinstance(summary.header.idt_all, float)
    assert isinstance(summary.header.wdt_TotTime, float)
    assert isinstance(summary.header.wdt_UsrTime, float)
    assert isinstance(summary.header.wdt_SysTime, float)
    assert isinstance(summary.header.chi2_Nl_eff, float)
    assert isinstance(summary.header.adev, float)
    assert isinstance(summary.header.sum_of_x, float)
    assert isinstance(summary.header.Flux_tot, float)
    assert isinstance(summary.header.Mini_tot, float)
    assert isinstance(summary.header.Mcor_tot, float)
    assert isinstance(summary.header.v0_min, float)
    assert isinstance(summary.header.vd_min, float)
    assert isinstance(summary.header.AV_min, float)
    assert isinstance(summary.header.YAV_min, float)

    assert isinstance(summary.data, Bunch)
    assert isinstance(summary.data.synthetic_spectrum, QTable)
    assert isinstance(
        summary.data.results_average_chains_xj, QTable
    )  # faltan nombre de columnas
    assert isinstance(
        summary.data.results_average_chains_mj, QTable
    )  # faltan nombre de columnas
    assert isinstance(
        summary.data.results_average_chains_Av_chi2_mass, QTable
    )  # faltan unidades
    assert isinstance(summary.data.synthetic_results, QTable)

    assert len(summary.data.synthetic_results) == 69
    assert len(summary.data.results_average_chains_xj) == 69
    assert len(summary.data.results_average_chains_mj) == 69
    assert len(summary.data.results_average_chains_Av_chi2_mass) == 9
    assert len(summary.data.synthetic_spectrum) == 1524

    assert isinstance(summary.age, float)
    assert isinstance(summary.reddening, float)
    assert isinstance(summary.av_value, float)
    assert isinstance(summary.normalization_point, float)
    assert isinstance(summary.z_value, float)

    assert isinstance(summary.spectra, Bunch)
    assert isinstance(summary.spectra.synthetic_spectrum, Spectrum1D)
    assert isinstance(summary.spectra.residual_spectrum, Spectrum1D)
    assert isinstance(summary.spectra.observed_spectrum, Spectrum1D)

    assert isinstance(summary.extra_info, Bunch)
    assert isinstance(summary.extra_info.xj_percent, int)
    assert isinstance(summary.extra_info.age_decimals, int)
    assert isinstance(summary.extra_info.rv, float)
    assert isinstance(summary.extra_info.z_decimals, int)
    assert isinstance(summary.extra_info.ssps_vector, pd.DataFrame)
    assert isinstance(summary.extra_info.synthesis_info, pd.DataFrame)


def test_is_float():
    assert starlight._is_float(np.random.randint(1, 100))


def test_is_float_none():
    assert not starlight._is_float(None)


"""
def test_convert_to_float(file_path):
    path = file_path("case_SC_Starlight_broken.out")

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Element at position (1) in ['2', 'novalue', "
            "'0.2377', '0.0000', '0.9042', '0.2231', '0.4009', "
            "'0.0000', '0.4409', '0.0000'] table cannot be "
            "converted to a number."
        ),
    ):
        starlight.read_starlight(path)
"""
