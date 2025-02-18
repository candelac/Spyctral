# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import pathlib
import sys
import datetime as dt


# add the spyctral source to the build path
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
SPYCTRAL_PATH = CURRENT_PATH.parent

sys.path.insert(0, str(SPYCTRAL_PATH))

UTC_NOW = dt.datetime.utcnow()


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Spyctral'
copyright = 'Copyright (c) 2023-2025 candelac'
author = 'Tapia, Martina'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'sphinx_mdinclude'
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']