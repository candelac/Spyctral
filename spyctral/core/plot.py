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
    """
    A class for generating plots from spectral data provided by a
    'SpectralSummary' object.
    It offers methods for visualizing one or multiple spectra in a customizable
    manner.

    Attributes
    ----------
    _summary : SpectralSummary
        An object containing the spectral data and additional information
        about the observed object.
    """

    _summary = attr.ib()

    def __call__(self, plot_kind="all_spectra", **kwargs):
        """
        Enables the class to be used as a function to generate different
        types of plots.
        Depending on the value of 'plot_kind', a specific method is invoked
        to generate the corresponding plot.

        Parameters
        ----------
        plot_kind : str, optional
            Type of plot to generate. Possible values are:
                - **"all_spectra"**: Plots all spectra.
                - **"single"**: Plots a specific spectrum.
                - **"split"**: Plots spectra with offsets.
                - **"subplots"**: Plots spectra in subplots.
        **kwargs
            Additional Parameters to pass to the plotting method.

        Returns
        -------
        object
            The plot generated by the corresponding method.
        """
        method = getattr(self, plot_kind)
        return method(**kwargs)

    def _set_common_labels(self, ax, title, obj_name):
        """
        Sets common labels and the title for plots, ensuring consistency in
        the generated plots.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis of the plot where the labels will be applied.
        title : str
            The title of the plot.
        obj_name : str
            The name of the observed object, included in the title.

        Returns
        -------
        None
            This method directly modifies the provided axes.
        """

        # Set common labels and titles for plots.
        ax.set_xlabel(r"Wavelength ($\AA$)")
        ax.set_ylabel("Flux")
        ax.set_title(f"{title} - {obj_name}")
        ax.grid(True)

    def _resolve_axis(self, ax, n_spectra):
        """
        Resolves and adjusts the axes for plots. If no axis is provided,
        this method creates new subplots for the specified number of spectra.

        Parameters
        ----------
        ax : matplotlib.axes.Axes or None
            The existing axis (or axes) for the plots. If None, new subplots
            will be created.
        n_spectra : int
            The number of spectra to be plotted.

        Returns
        -------
        numpy.ndarray
            An array of axes for the plots.
        """
        if ax is None:
            fig, ax = plt.subplots(n_spectra, 1, sharex=True)
            size_x, size_y = fig.get_size_inches()
            fig.set_size_inches(size_x, size_y * n_spectra)
        if not isinstance(ax, Iterable):
            ax = [ax]
        return np.asarray(ax)

    def all_spectra(self, ax=None, **kwargs):
        """
        Plots all spectra stored in the 'spectra' attribute of the associated
        object. Each spectrum is represented on the same plot with a legend.

        Parameters
        ----------
        ax : matplotlib.axes.Axes or None
            The axis where the spectra will be plotted. If None, the current
            axis ('plt.gca()') is used.
        **kwargs
            Additional parameters to customize the plot style
            (e.g., color, line type, etc.).

        Returns
        -------
        matplotlib.axes.Axes
            The axis containing the plot of all spectra.

        Methods
        -------
            __call__()
                Calls a plotting method based on the specified type.
            all_spectra()
                Plots all spectra together.
            single()
                Plots a specific spectrum.
            split()
                Plots spectra with an offset.
            subplots()
                Divides spectra into individual subplots.
        """
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
        """
        Plots a single spectrum identified by its name. The spectrum is
        retrieved from the 'spectra' attribute and displayed on the
        specified axis.

        Parameters
        ----------
        spectrum_name : str
            The name of the spectrum to be plotted.
        ax : matplotlib.axes.Axes or None
            The axis where the spectrum will be plotted. If None, the current
            axis ('plt.gca()') is used.
        **kwargs
            Additional parameters to customize the plot style
                (e.g., color, line type, etc.).

        Returns
        -------
        matplotlib.axes.Axes
            The axis containing the plot of the requested spectrum.
        """
        spectra = self._summary.spectra

        spectrum = spectra[spectrum_name]

        ax = plt.gca() if ax is None else ax
        ax.plot(spectrum.spectral_axis, spectrum.flux, **kwargs)
        self._set_common_labels(ax, spectrum_name, self._summary.obj_name)
        # plt.show()
        return ax

    def split(self, offset=0.1, ax=None, **kwargs):
        """
        Plots multiple spectra, applying an incremental vertical offset to
        each spectrum (except for residual spectra) to facilitate comparative
        visualization.

        Parameters
        ----------
        offset : float, optional
            The vertical offset applied between spectra. Default is 0.1.
        ax : matplotlib.axes.Axes or None
            The axis where the spectra will be plotted. If None, the current
            axis ('plt.gca()') is used.
        **kwargs
            Additional parameters to customize the plot style
            (e.g., color, line type, etc.).

        Returns
        -------
        matplotlib.axes.Axes
            The axis containing the plotted offset spectra.

        Notes
        -----
        This method is useful for highlighting differences between spectra by
        reducing overlapping curves.
        """
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
        """
        Creates individual subplots for each spectrum, allowing separate
        visualization for each one. All subplots share the same x-axis
        (wavelength).

        Parameters
        ----------
        ax : matplotlib.axes.Axes or None
            The set of axes where the spectra will be plotted. If None, new
            subplots are automatically created.
        **kwargs
            Additional parameters to customize the plot style
                (e.g., color, line type, etc.).

        Returns
        -------
        numpy.ndarray
                An array of 'Axes' objects corresponding to the subplots.

        Notes
        -----
        This method enables the individual analysis of each spectrum in
        separate plots, which is useful for examining specific details without
        overlapping others.
        """
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

        ax[n_spectra - 1].set_xlabel(r"Wavelength ($\AA$)")
        ax[0].set_title(self._summary.obj_name)
        # plt.show()
        return ax
