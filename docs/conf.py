# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import pathlib
import sys
import datetime as dt


# add the skcriteria source to the build path
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
SPYCTRAL_PATH = CURRENT_PATH.parent.parent

sys.path.insert(0, str(SPYCTRAL_PATH))


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
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

import m2r2

DYNAMIC_RST = {
    "README.md": "README.rst"
}

for md_name, rst_name in DYNAMIC_RST.items():
    md_path = SPYCTRAL_PATH / md_name
    with open(md_path) as fp:
        readme_md = fp.read().split("<!-- BODY -->", 1)[-1]

    rst_path = CURRENT_PATH / "_dynamic" / rst_name

    with open(rst_path, "w") as fp:
        fp.write(".. FILE AUTO GENERATED !! \n")
        fp.write(m2r2.convert(readme_md))
        print(f"{md_path} -> {rst_path} regenerated!")