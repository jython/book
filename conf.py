# -*- coding: utf-8 -*-


extensions = []
templates_path = ['/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx', 'templates', '_templates', '.templates']
source_suffix = ['.rst']		
master_doc = 'index'
project = u'jython'
copyright = u'2016'
version = 'latest'
release = 'latest'
exclude_patterns = ['_build','sandbox']
pygments_style = 'sphinx'
htmlhelp_basename = 'jython'
html_theme = 'sphinx_rtd_theme'
file_insertion_enabled = False
latex_documents = [
  ('index', 'jython.tex', u'jython Documentation',
   u'', 'manual'),
]

