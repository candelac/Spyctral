# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

"""Test plots."""

# =============================================================================
# IMPORTS
# =============================================================================


import spyctral as spy


def test_all_plots_fisa(file_path):
    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    axis = summary.plot()

    suptitle = axis.get_figure()._suptitle.get_text()
    title = axis.get_title()
    xlabel = axis.get_xlabel()
    ylabel = axis.get_ylabel()

    assert suptitle == "FISA"
    assert title == "All Spectra"
    assert xlabel == "Wavelength (Angstrom)"
    assert ylabel == "Flux"


def test_all_plots_starlight(file_path):
    path = file_path("case_SC_Starlight.out")

    summary = spy.read_starlight(path)

    axis = summary.plot()

    suptitle = axis.get_figure()._suptitle.get_text()
    title = axis.get_title()
    xlabel = axis.get_xlabel()
    ylabel = axis.get_ylabel()

    assert suptitle == "Starlight"
    assert title == "All Spectra"
    assert xlabel == "Wavelength (Angstrom)"
    assert ylabel == "Flux"


def test_single_plots_fisa(file_path):
    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    axists = summary.plot.single("Template_spectrum")
    axisos = summary.plot.single("Observed_spectrum")
    axisus = summary.plot.single("Unreddened_spectrum")
    axistrs = summary.plot.single("Residual_flux")

    suptitlet = axists.get_figure()._suptitle.get_text()
    titlets = axists.get_title()
    xlabelts = axists.get_xlabel()
    ylabelts = axists.get_ylabel()

    suptitleo = axisos.get_figure()._suptitle.get_text()
    titleos = axisos.get_title()
    xlabelos = axisos.get_xlabel()
    ylabelos = axisos.get_ylabel()

    suptitleu = axisus.get_figure()._suptitle.get_text()
    titleus = axisus.get_title()
    xlabelus = axisus.get_xlabel()
    ylabelus = axisus.get_ylabel()

    suptitler = axistrs.get_figure()._suptitle.get_text()
    titlers = axistrs.get_title()
    xlabelrs = axistrs.get_xlabel()
    ylabelrs = axistrs.get_ylabel()

    assert suptitlet == "FISA"
    assert titlets == "Spectrum Template_spectrum"
    assert xlabelts == "Wavelength (Angstrom)"
    assert ylabelts == "Flux"

    assert suptitleo == "FISA"
    assert titleos == "Spectrum Observed_spectrum"
    assert xlabelos == "Wavelength (Angstrom)"
    assert ylabelos == "Flux"

    assert suptitleu == "FISA"
    assert titleus == "Spectrum Unreddened_spectrum"
    assert xlabelus == "Wavelength (Angstrom)"
    assert ylabelus == "Flux"

    assert suptitler == "FISA"
    assert titlers == "Spectrum Residual_flux"
    assert xlabelrs == "Wavelength (Angstrom)"
    assert ylabelrs == "Flux"


def test_single_plots_starlight(file_path):
    path = file_path("case_SC_Starlight.out")

    summary = spy.read_starlight(path)

    axisos = summary.plot.single("observed_spectrum")
    axisus = summary.plot.single("synthetic_spectrum")
    axistrs = summary.plot.single("residual_spectrum")

    suptitleo = axisos.get_figure()._suptitle.get_text()
    titleos = axisos.get_title()
    xlabelos = axisos.get_xlabel()
    ylabelos = axisos.get_ylabel()

    suptitleu = axisus.get_figure()._suptitle.get_text()
    titleus = axisus.get_title()
    xlabelus = axisus.get_xlabel()
    ylabelus = axisus.get_ylabel()

    suptitler = axistrs.get_figure()._suptitle.get_text()
    titlers = axistrs.get_title()
    xlabelrs = axistrs.get_xlabel()
    ylabelrs = axistrs.get_ylabel()

    assert suptitleo == "Starlight"
    assert titleos == "Spectrum observed_spectrum"
    assert xlabelos == "Wavelength (Angstrom)"
    assert ylabelos == "Flux"

    assert suptitleu == "Starlight"
    assert titleus == "Spectrum synthetic_spectrum"
    assert xlabelus == "Wavelength (Angstrom)"
    assert ylabelus == "Flux"

    assert suptitler == "Starlight"
    assert titlers == "Spectrum residual_spectrum"
    assert xlabelrs == "Wavelength (Angstrom)"
    assert ylabelrs == "Flux"
