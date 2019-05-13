# -*- coding: utf-8 -*-


extensions = []
templates_path = ['_templates']
source_suffix = ['.rst']		
master_doc = 'index'

project = u'Definitive Guide to Jython'
copyright = u'2010, 2019'
version = 'latest'
release = 'latest'

exclude_patterns = ['_build','sandbox']

pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
file_insertion_enabled = False


# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = 'jython'


# -- Options for LaTeX output ------------------------------------------------
# LaTeX is intermediate to the PDF output

latex_documents = [
    # (startdocname, targetname, title, author, documentclass, toctree_only)
    (   'index', 'jython.tex',
        u'The Definitive Guide to Jython',
        u'Josh Juneau, Jim Baker, Victor Ng, Leo Soto, Frank Wierzbicki',
        'manual',
        False),
]

