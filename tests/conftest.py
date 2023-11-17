#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2023, Cerdosino Candela, Fiore J.Manuel, Martinez J.Luis,
# Tapia-Reina Martina
# All rights reserved.

import pytest

from .datasets import PATH


@pytest.fixture(scope="session")
def file_path():
    def _maker(fname):
        return PATH / fname

    return _maker
