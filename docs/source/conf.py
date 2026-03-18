# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://sphinx-doc.org/en/master/usage/configuration.html#project-information

import bmlite as bm

project = 'BATMODS-lite'
author = 'Corey R. Randall'
copyright = 'Alliance for Energy Innovation, LLC'

version = bm.__version__
release = bm.__version__

# json_url = 'https://batmods-lite.readthedocs.io/en/latest/_static/switcher.json'


# -- General configuration ---------------------------------------------------
# https://sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon', 
    'sphinx.ext.viewcode',
    'myst_nb', 
    'sphinx_design',
    # 'sphinx_favicon',
    'sphinx_copybutton',
    'autoapi.extension', 
]

templates_path = ['_templates']

exclude_patterns = [
    'build', 
    'Thumbs.db', 
    '.DS_Store', 
    '__pycache__',
    '*.ipynb_checkpoints',
]

source_suffix = {
    '.myst': 'myst-nb',
    '.ipynb': 'myst-nb',
    '.rst': 'restructuredtext',
}

default_role = 'literal'  # allow single backticks for inline code refs
highlight_language = 'console'


# -- Options for HTML output -------------------------------------------------
# https://sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html

html_theme = 'pydata_sphinx_theme'

# html_favicon = '_static/favicon.ico'
html_context = {'default_mode': 'dark'}

html_static_path = ['_static']

html_js_files = ['custom.js']
html_css_files = ['custom.css']

html_sidebars = {'index': [], '**': ['sidebar-nav-bs']}

html_theme_options = {
    # 'logo': {
    #     'image_light': '_static/light_notag.svg',
    #     'image_dark': '_static/dark_notag.svg',
    # },
    'icon_links': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/NatLabRockies/batmods-lite',
            'icon': 'fa-brands fa-github',
        },
        # {
        #     'name': 'PyPI',
        #     'url': 'https://pypi.org/project/batmods-lite',
        #     'icon': 'fa-solid fa-box',
        # },
    ],
    'navbar_start': ['navbar-logo'],
    'navbar_align': 'content',
    'header_links_before_dropdown': 5, 
    'footer_start': ['copyright'],
    'footer_end': ['sphinx-version'],
    'navbar_persistent': ['search-button-field'],
    'primary_sidebar_end': ['sidebar-ethical-ads'],
    'secondary_sidebar_items': ['page-toc'],
    'search_bar_text': 'Search...',
    'show_prev_next': False,
    'collapse_navigation': True,
    'show_toc_level': 0,
    'pygments_light_style': 'tango',
    # 'show_version_warning_banner': True,
    # 'switcher': {
    #     'json_url': json_url,
    #     'version_match': version,
    # }
}


# -- Options for napoleon ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_numpy_docstring = True
napoleon_custom_sections = [
    'BATMODS-lite', 
    'How to use the documentation', 
    'Viewing documentation using IPython',
    'Material Properties Package',
    'Math Module',
    'Mesh Module',
    'Plotting Utilities',
    'Single Particle Model Package',
    'Pseudo-2D Model Package',
    'Domains Module',
    'DAE Module',
    'Root Functions',
    'Post-processing Utilities',
    'Solution Classes',
    ]


# -- Options for autoapi -----------------------------------------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html

autoapi_root = 'api'
autoapi_type = 'python'
autoapi_keep_files = True 
autodoc_typehints = 'none'
autoapi_member_order = 'groupwise'
autoapi_python_class_content = 'both'
autoapi_dirs = ['../../src/bmlite']
autoapi_options = [
    'members',
    'imported-members',
    'inerited-members',
    'show-module-summary',
]


# -- Options for myst --------------------------------------------------------
# https://myst-nb.readthedocs.io/en/latest/configuration.html

nb_execution_timeout = 300
nb_number_source_lines = True
myst_enable_extensions = ['amsmath', 'dollarmath']