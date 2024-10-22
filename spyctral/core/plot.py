# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# IMPORTS
# =============================================================================

from collections.abc import Iterable

import attr

import matplotlib.pyplot as plt

import numpy as np

# =============================================================================
# CLASSES
# =============================================================================


@attr.s(repr=False)
class SpectralPlotter:
    _summary = attr.ib()

    def __repr__(self):
        return f"SpectralPlotter(summary{hex(id(self._summary))})"

    def __call__(self, plot_kind="all_spectra", **kwargs):
        method = getattr(self, plot_kind)
        return method(**kwargs)

    def _set_common_labels(self, ax, title, obj_name):
        """Set common labels and titles for plots."""
        ax.set_xlabel(r"Wavelength ($\AA$)")
        ax.set_ylabel("Flux")
        ax.set_title(f"{title} - {obj_name}")
        ax.grid(True)

    def _resolve_axis(self, ax, n_spectra):
        """Resolve the axis for plotting."""
        if ax is None:
            fig, ax = plt.subplots(
                n_spectra, 1, figsize=(10, 4 * n_spectra), sharex=True
            )
            size_x, size_y = fig.get_size_inches()
            fig.set_size_inches(size_x, size_y * n_spectra)
        if not isinstance(ax, Iterable):
            ax = [ax]
        return np.asarray(ax)

    def all_spectra(self, ax=None, **kwargs):
        spectra = self._summary.spectra

        ax = plt.gca() if ax is None else ax
        # kwargs.setdefault("-")
        for name, spectrum in spectra.items():
            ax.plot(
                spectrum.spectral_axis, spectrum.flux, label=name, **kwargs
            )
        self._set_common_labels(ax, "All spectra", self._summary.obj_name)
        ax.legend()
        # plt.show()
        return ax

    def single(self, spectrum_name, ax=None, **kwargs):
        spectra = self._summary.spectra

        spectrum = spectra[spectrum_name]

        ax = plt.gca() if ax is None else ax
        ax.plot(spectrum.spectral_axis, spectrum.flux, **kwargs)
        self._set_common_labels(ax, spectrum_name, self._summary.obj_name)
        # plt.show()
        return ax

    def split(self, offset=0.1, ax=None, **kwargs):
        spectra = self._summary.spectra

        ax = plt.gca() if ax is None else ax
        cumulative_offset = 0
        for name, spectrum in spectra.items():
            if name not in ["residual_spectrum", "Residual_flux"]:
                cumulative_offset += offset
            else:
                cumulative_offset = 0

            ax.plot(
                spectrum.spectral_axis,
                spectrum.flux + cumulative_offset,
                label=name,
                **kwargs,
            )
        self._set_common_labels(
            ax, "Spectra with offset", self._summary.obj_name
        )
        ax.legend()
        # plt.show()
        return ax

    def subplots(self, ax=None, **kwargs):
        spectra = self._summary.spectra
        n_spectra = len(spectra)

        ax = self._resolve_axis(ax, n_spectra)

        for ax_i, (name, spectrum) in zip(ax, spectra.items()):
            ax_i.plot(
                spectrum.spectral_axis, spectrum.flux, label=name, **kwargs
            )
            ax_i.set_ylabel("Flux")
            ax_i.legend()
            ax_i.grid(True)

        plt.xlabel(r"Wavelength ($\AA$)")
        plt.suptitle(self._summary.obj_name)
        # plt.show()
        return ax
