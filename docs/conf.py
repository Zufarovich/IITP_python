# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'Image interpolation'
copyright = '2025, Shamsutdinov Amir'
author = 'Shamsutdinov Amir'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser',
              'myst_parser', 
            'sphinx_click',
            'sphinx_rtd_theme',
            'sphinx.ext.viewcode',
            'sphinx.ext.autodoc',
            'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_type_aliases = {
    'Path': 'pathlib.Path',
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

myst_enable_extensions = [
    "amsmath",      # Для окружений LaTeX типа align, equation и т.д.
    "dollarmath",   # Для $...$ (inline) и $$...$$ (display) математики
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
