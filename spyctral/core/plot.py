# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import matplotlib.pyplot as plt
import attr
import numpy as np


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
        ax.set_title(title)
        plt.suptitle(self._get_file_type())
        ax.grid(True)

    def single(self, spectrum_name, **kwargs):
        spectra = self._summary.spectra

        if spectrum_name not in spectra:
            raise ValueError(
                f"Spectrum '{spectrum_name}' not found in spectra.")
        spectrum = spectra[spectrum_name]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(spectrum.spectral_axis, spectrum.flux, **kwargs)
        self._set_common_labels(ax, f"Spectrum {spectrum_name}")

        plt.show()
        return ax

    def all(self, **kwargs):
        spectra = self._summary.spectra

        fig, ax = plt.subplots(figsize=(10, 6))
        for name, spectrum in spectra.items():
            ax.plot(spectrum.spectral_axis,
                    spectrum.flux, label=name, **kwargs)
        self._set_common_labels(ax, "All Spectra")
        ax.legend()
        plt.show()
        return ax

    def split(self, offset=0.1, **kwargs):
        spectra = self._summary.spectra
        fig, ax = plt.subplots(figsize=(10, 6))
        cumulative_offset = 0
        for name, spectrum in spectra.items():
            if name not in ["residual_spectrum", "Residual_flux"]:
                cumulative_offset += offset
            else:
                cumulative_offset = 0
            ax.plot(spectrum.spectral_axis, spectrum.flux +
                    cumulative_offset, label=name, **kwargs)
        ax.set_ylabel("Flux (Offset Applied)")
        self._set_common_labels(ax, "Spectra with Offset")
        ax.legend()
        plt.show()
        return ax

    def subplots(self, **kwargs):
        spectra = self._summary.spectra
        n = len(spectra)
        fig, axes = plt.subplots(n, 1, figsize=(10, 4 * n), sharex=True)
        plt.suptitle(self._get_file_type())

        if n == 1:
            axes = [axes]

        for ax, (name, spectrum) in zip(axes, spectra.items()):
            ax.plot(spectrum.spectral_axis,
                    spectrum.flux, label=name, **kwargs)
            ax.set_ylabel("Flux")
            ax.legend()
            ax.grid(True)

        plt.xlabel("Wavelength (Angstrom)")
        plt.show()
        return ax

        # def plot(self, color=["sienna", "plum", "olive", "blue"],
        #          styleline='-', grid='False'):
        #    """
        #    Plots spectrum from Starlight and FISA
        #    usage: plot()
        #           plot([<color1>, <color2>, <color3>, <color3>]"")
        #           plot([<color1>, <color2>, <color3>, <color3>], <styleline>)
        #    return: plot matplotlib.pyplot style
        #    """
        #    spectra = self.spectra
        #    # ["synthetic_spectrum", "observed_spectrum", "residual_spectrum"]
        #    spect_names = list(spectra.keys())
        #    fig, ax = plt.subplots(figsize=(22, 10))
        #
        #    if len(spect_names) == 3:
        #        fig.suptitle("Gráficos de Starlight")
        #    else:
        #        fig.suptitle("Gráficos de FISA")
        #    current_ax = 0
        #    for valores in spectra:
        #        ax = fig.axes[0]
        #        ax.plot(
        #            spectra[valores].spectral_axis,
        #            spectra[valores].flux,
        #            label=spect_names[current_ax],
        #            color=color[current_ax],
        #            linewidth=1,
        #            linestyle=styleline
        #        )
        #        current_ax += 1
        #    ax.set_xlabel("Longitud de onda(Angstrom)")
        #    ax.axhline(y=0, color='grey', linestyle=styleline, label='y=0')
        #    ax.set_ylabel('Flux')
        #    ax.legend()
        #    ax.grid(grid)
        #    plt.show()
        # def plotPd(self, color=["sienna", "plum", "olive", "blue"],
        #           styleline='-', _grid=False,
        #           xlim=None, ylim=None):
        # Ejemplo de uso
        # Suponiendo que 'star' es una instancia de SpectralSummary y tiene
        # los datos cargados
        # star = spy.read_starlight('tests/datasets/case_SC_Starlight.out')
        # star.plotSL(xlim=(3000, 7000), ylim=(-1.2, 1.2))
        #    spectra = self.spectra
        #    # Obtener dinámicamente los nombres
        #    spect_names = list(spectra.keys())
        # Determinar el título dinámicamente
        #    if len(spect_names) == 3:
        #        _title = "Gráficos de Starlight"
        #    else:
        #        _title = "Gráficos de FISA"
        #    # Crear un DataFrame vacío para inicializar el plot
        #    df_empty = pd.DataFrame({'wavelength': [], 'flux': []})
        #    ax = df_empty.plot(x='wavelength', y='flux')  # Crear el subplot vacío
        #    # Graficar cada espectro por separado
        #    for idx, name in enumerate(spect_names):
        #        df = pd.DataFrame({
        #            'wavelength': spectra[name].spectral_axis.value,
        #            'flux': spectra[name].flux.value
        #        })
        #        # Crear el plot usando pandas
        #        df.plot(x='wavelength', y='flux', ax=ax,
        #                color=color[idx], linestyle=styleline, label=name,
        #                title=_title, grid=_grid)
        #    ax.set_xlabel("Longitud de onda (Angstrom)")
        #    ax.set_ylabel('Flux')
        #    ax.axhline(y=0, color='grey', linestyle=styleline, label='y=0')
        #    # Configurar límites de los ejes si se proporcionan
        #    if xlim:
        #        ax.set_xlim(xlim)
        #    if ylim:
        #        ax.set_ylim(ylim)
        #    ax.legend(spect_names)
