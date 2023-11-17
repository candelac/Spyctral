#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import re

import pandas as pd

from spyctral import core

from astropy.table import QTable
import astropy.units as u


RM_SCHAR_R = re.compile( r"[\[]")
RX_SRBM = re.compile(r'.*Synthesis Results - Best model.*')
RX_SS = re.compile(r'.*Synthetic spectrum.*')

def read_star_light(path):
    """Recives a path to a .out file from star light software divides it in to tree categories
    and returns a summaryfunction object
"""
    title_summary, title_spectrum = [],[]
    best_summary, best_spectrum = [], []
    start_app_summary = None
    start_app_spectrum = None

    input_info_dict = {}
    with open(path) as starfile:
        for starline in starfile:

            start_append_summary=re.match(RX_SRBM, starline)
            start_append_spectrum = re.match(RX_SS, starline)
            
            if start_append_summary is not None and start_append_summary[0] != ' ':
                start_app_summary = start_append_summary[0]
            if start_append_spectrum is not None and start_append_spectrum[0] != ' ':
                start_app_spectrum = start_append_spectrum[0]

            if start_app_summary is not None and start_app_spectrum is None:
                if RM_SCHAR_R.search(starline) is None:
                    if starline.startswith('#'):
                        title_summary.append(starline)
                    else:
                        best_summary.append(starline.replace('\n',''))
                    
            if start_app_summary is not None and start_app_spectrum is not None:
                if RM_SCHAR_R.search(starline) is None:
                    if starline.startswith('#'):
                        title_spectrum.append(starline)
                    else:
                        best_spectrum.append(starline.replace('\n','').split('   '))

            if starline.startswith('#') is not True:
                 starline = starline.replace(']','').replace('\n','').split('[')
                 if len(starline) > 1:
                    input_info_dict[starline[1]] = starline[0].strip()
    
    spectra_table = QTable(rows=best_spectrum, names=['l_obs','f_obs','f_syn','weights'])
    spectra_table['l_obs'].unit = u.Angstrom
    print(len(best_summary))
    return input_info_dict , best_summary, spectra_table

inf, bts, bsts = read_star_light(r'C:\Users\fiore\OneDrive\Desktop\cursos\spyctral\add_on\case_SC_Starlight.out')

#print(inf)