# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

# =============================================================================
# IMPORTS
# =============================================================================

import attr

import matplotlib.pyplot as plt

# =============================================================================
# CLASSES
# =============================================================================


@attr.s(repr=False)
class SpectralPlotter:
    _summary = attr.ib()

    def __repr__(self):
        return f"SpectralPlotter(summary{hex(id(self._summary))})"

    def __call__(self, kind="all", **kwargs):
        method = getattr(self, kind)
        return method(**kwargs)

    def _get_file_type(self):
        """Determine the file type based on the spectra length."""
        spect_names = list(self._summary.spectra.keys())
        if len(spect_names) == 3:
            return "Starlight"
        else:
            return "FISA"

    def _set_common_labels(self, ax, title):
        ax.set_xlabel("Wavelength (Angstrom)")
        ax.set_ylabel("Flux")
        ax.set_title(title + " - " + self._get_file_type())
        # plt.suptitle(self._get_file_type())
        ax.grid(True)

    def all_spectra(self, ax=None, **kwargs):
        spectra = self._summary.spectra

        ax = plt.gca() if ax is None else ax
        # kwargs.setdefault("-")
        for name, spectrum in spectra.items():
            ax.plot(
                spectrum.spectral_axis, spectrum.flux, label=name, **kwargs
            )
        self._set_common_labels(ax, "All Spectra")
        ax.legend()
        # plt.show()
        return ax

    def single(self, spectrum_name, ax=None, **kwargs):
        spectra = self._summary.spectra

        if spectrum_name not in spectra:
            raise ValueError(
                f"Spectrum '{spectrum_name}' not found in spectra."
            )
        else:
            spectrum = spectra[spectrum_name]

        ax = plt.gca() if ax is None else ax
        ax.plot(spectrum.spectral_axis, spectrum.flux, **kwargs)
        self._set_common_labels(ax, f"Spectrum {spectrum_name}")
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
        self._set_common_labels(ax, "Spectra with Offset")
        ax.legend()
        # plt.show()
        return ax

    # def subplots(self, ax= None, **kwargs):
    #    spectra = self._summary.spectra
    #    n = len(spectra)

    #    fig, ax = plt.subplots(n, 1, figsize=(10, 4 * n), sharex=True)
    #    plt.suptitle(self._get_file_type())

    #    if n == 1:
    #        ax = [ax]

    #    for ax_i, (name, spectrum) in zip(ax, spectra.items()):
    #        ax_i.plot(
    #            spectrum.spectral_axis, spectrum.flux, label=name, **kwargs
    #        )
    #        ax_i.set_ylabel("Flux")
    #        ax_i.legend()
    #        ax_i.grid(True)

    #    fig.supxlabel("Wavelength (Angstrom)")
    # plt.show()
    #    return ax
