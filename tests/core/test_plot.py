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

from unittest import mock

# import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal

import numpy as np

import pytest

import spyctral as spy


# =============================================================================
# SpectralPlotter TESTS
# =============================================================================


@pytest.mark.parametrize("plot_kind", ["all_spectra"])
def test_spectralplotter_call(file_path, plot_kind):
    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    plotter = spy.core.plot.SpectralPlotter(summary)

    method_name = f"spyctral.core.plot.SpectralPlotter.{plot_kind}"

    with mock.patch(method_name) as plot_method:
        plotter(plot_kind=plot_kind)

    plot_method.assert_called_once()


def test_spectralplotter_resolve_axis_with_none(file_path):
    """Test when ax is None, with FISA file."""
    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    plotter = spy.core.plot.SpectralPlotter(summary)

    n_spectra = len(summary.spectra)

    ax = plotter._resolve_axis(None, n_spectra)

    assert isinstance(ax, np.ndarray)
    assert len(ax) == n_spectra


# def test_spectralplotter_resolve_axis_iterable(file_path):
#    """Test when ax is an iterable."""
#    path = file_path("case_SC_FISA.fisa")

#    summary = spy.read_fisa(path)

#    plotter = spy.core.plot.SpectralPlotter(summary)

#    fig, axes = plt.subplots(2)

#    ax = plotter._resolve_axis(axes, 2)

#    assert isinstance(ax, np.ndarray)
#    assert ax.all() == axes.all()


@check_figures_equal(extensions=["png"])
def test_spectralplotter_all_spectra(file_path, fig_test, fig_ref):
    """Test the all_spectra function with a FISA file"""

    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    plotter = spy.core.plot.SpectralPlotter(summary)

    # test
    test_ax = fig_test.subplots()
    plotter.all_spectra(ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()

    for spectrum_name, spectrum in summary.spectra.items():
        exp_ax.plot(spectrum.spectral_axis, spectrum.flux, label=spectrum_name)
        exp_ax.set_xlabel(r"Wavelength ($\AA$)")
        exp_ax.set_ylabel("Flux")
        exp_ax.set_title("All spectra - object_1")
        exp_ax.grid(True)
    exp_ax.legend()


@check_figures_equal(extensions=["png"])
def test_spectralplotter_single_template_spectrum(
    file_path, fig_test, fig_ref
):
    """Test the single("Template_spectrum") function with a FISA file"""

    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    plotter = spy.core.plot.SpectralPlotter(summary)

    # test
    test_ax = fig_test.subplots()
    plotter.single("Template_spectrum", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()

    spectrum = summary.spectra["Template_spectrum"]

    exp_ax.plot(spectrum.spectral_axis, spectrum.flux)
    exp_ax.set_xlabel(r"Wavelength ($\AA$)")
    exp_ax.set_ylabel("Flux")
    exp_ax.set_title("Template_spectrum - object_1")
    exp_ax.grid(True)


@check_figures_equal(extensions=["png"])
def test_spectralplotter_split(file_path, fig_test, fig_ref):
    """Test the split function with a FISA file."""

    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    plotter = spy.core.plot.SpectralPlotter(summary)

    # test
    test_ax = fig_test.subplots()
    plotter.split(offset=1, ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()

    spectrum_residual_flux = summary.spectra["Residual_flux"]
    spectrum_unreddened = summary.spectra["Unreddened_spectrum"]
    spectrum_template = summary.spectra["Template_spectrum"]
    spectrum_observed = summary.spectra["Observed_spectrum"]

    exp_ax.plot(
        spectrum_unreddened.spectral_axis,
        spectrum_unreddened.flux + 1,
        label="Unreddened_spectrum",
    )
    exp_ax.plot(
        spectrum_template.spectral_axis,
        spectrum_template.flux + 2,
        label="Template_spectrum",
    )
    exp_ax.plot(
        spectrum_observed.spectral_axis,
        spectrum_observed.flux + 3,
        label="Observed_spectrum",
    )
    exp_ax.plot(
        spectrum_residual_flux.spectral_axis,
        spectrum_residual_flux.flux,
        label="Residual_flux",
    )

    exp_ax.set_xlabel(r"Wavelength ($\AA$)")
    exp_ax.set_ylabel("Flux")
    exp_ax.set_title("Spectra with offset - object_1")
    exp_ax.grid(True)
    exp_ax.legend()


@check_figures_equal(extensions=["png"])
def test_spectralplotter_subplots(file_path, fig_test, fig_ref):
    """Test the subplots function with a FISA file."""

    path = file_path("case_SC_FISA.fisa")

    summary = spy.read_fisa(path)

    plotter = spy.core.plot.SpectralPlotter(summary)

    # test
    test_axes = fig_test.subplots(4, 1, sharex=True)
    plotter.subplots(ax=test_axes)

    # expected
    exp_axes = fig_ref.subplots(4, 1, sharex=True).flatten()

    spectrum_unreddened = summary.spectra["Unreddened_spectrum"]
    spectrum_template = summary.spectra["Template_spectrum"]
    spectrum_observed = summary.spectra["Observed_spectrum"]
    spectrum_residual_flux = summary.spectra["Residual_flux"]

    exp_axes[0].plot(
        spectrum_unreddened.spectral_axis,
        spectrum_unreddened.flux,
        label="Unreddened_spectrum",
    )
    exp_axes[0].set_ylabel("Flux")
    exp_axes[0].grid(True)
    exp_axes[0].legend()
    exp_axes[0].set_title("object_1")

    exp_axes[1].plot(
        spectrum_template.spectral_axis,
        spectrum_template.flux,
        label="Template_spectrum",
    )
    exp_axes[1].set_ylabel("Flux")
    exp_axes[1].grid(True)
    exp_axes[1].legend()

    exp_axes[2].plot(
        spectrum_observed.spectral_axis,
        spectrum_observed.flux,
        label="Observed_spectrum",
    )
    exp_axes[2].set_ylabel("Flux")
    exp_axes[2].grid(True)
    exp_axes[2].legend()

    exp_axes[3].plot(
        spectrum_residual_flux.spectral_axis,
        spectrum_residual_flux.flux,
        label="Residual_flux",
    )
    exp_axes[3].set_ylabel("Flux")
    exp_axes[3].grid(True)
    exp_axes[3].legend()
    exp_axes[3].set_xlabel(r"Wavelength ($\AA$)")
