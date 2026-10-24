# DexSuite documentation. Built by Read the Docs from docs/source (see .readthedocs.yaml).
# Local build:  sphinx-build -b html docs/source docs/_build/html

project = "DexSuite"
author = "DexSuite authors"
copyright = "2026, DexSuite authors"
release = "0.1"

extensions = [
    "myst_parser",          # pages are Markdown (MyST)
    "sphinx_design",        # grids, cards, tabs
    "sphinx_copybutton",
]
myst_enable_extensions = ["colon_fence", "deflist", "attrs_inline", "attrs_block", "fieldlist"]
myst_heading_anchors = 3
exclude_patterns = ["_build", "**/_partials/*"]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
suppress_warnings = ["myst.header"]

# -- HTML -------------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = "DexSuite"
html_static_path = ["_static"]
html_favicon = "_static/brand/favicon.svg"
html_css_files = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
    "css/dexsuite.css",
]
html_js_files = ["js/dexsuite.js"]

html_theme_options = {
    "logo": {
        "image_light": "_static/brand/wordmark.svg",
        "image_dark": "_static/brand/wordmark.svg",
        "alt_text": "DexSuite",
    },
    "header_links_before_dropdown": 7,
    "navbar_align": "left",
    "navbar_end": ["navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "show_prev_next": True,
    "show_toc_level": 2,
    "navigation_depth": 3,
    "collapse_navigation": False,
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "use_edit_page_button": True,
    "footer_start": ["copyright"],
    "footer_end": [],
    "pygments_light_style": "friendly",
    "icon_links": [
        {"name": "Project page", "url": "https://dexsuiteorg.github.io/", "icon": "fa-solid fa-globe", "type": "fontawesome"},
        {"name": "Datasets on Hugging Face", "url": "https://huggingface.co/dexsuite", "icon": "fa-solid fa-database", "type": "fontawesome"},
        {"name": "GitHub", "url": "https://github.com/dexsuiteorg", "icon": "fa-brands fa-github", "type": "fontawesome"},
    ],
}
html_context = {
    "default_mode": "light",          # the project page is light only, so are the docs
    "github_user": "dexsuiteorg",
    "github_repo": "docs",
    "github_version": "main",
    "doc_path": "docs/source",
}
html_sidebars = {"index": [], "**": ["sidebar-nav-bs"]}

copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True
