import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'i3pie'
copyright = '2019, Giacomo Comitti'
author = 'Giacomo Comitti'
release = '0.1'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
html_theme = 'classic'
