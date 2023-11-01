#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

#aca van los fixtures

@pytest.fixtur(scope="session")
def data_path():
    def_data_path(filename):
        return PATH / filename
    return
def read_box()

    def _reader(filename):
        filepath= PATH / filename
        return 


--

def test(data_path):
    path=data_path('data-random')
    vox=read_atable(path)
    assert isinstance(box,box.Box)
    assert len(box) == 1

    evaluar el archivo: len, 