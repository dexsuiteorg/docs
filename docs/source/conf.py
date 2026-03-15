# -- Project info -----------------------------------------------------------
project = "Dexsuite"
author = "Dexsuite team"
release = "latest"   # e.g., "0.1.0" later

# -- General config ---------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- HTML theme -------------------------------------------------------------
html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]  # keep, even if empty, to add versions.json/logo later
html_css_files = ["css/custom.css"]

# Repo / "Edit on GitHub" button
html_theme_options = {
    "logo": {
        "text": "Dexsuite",
    },
    "use_edit_page_button": True,
    "show_prev_next": False,
    "show_nav_level": 2,
    "navbar_center": [],

    # Keep the header simple for local builds (no version switcher dropdown).
    "navbar_end": ["navbar-icon-links", "theme-switcher"],

    # Right-side icon links
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/your-org/dexsuite",  # <-- change later
            "icon": "fab fa-github",
            "type": "fontawesome",
        },
    ],
}

html_sidebars = {
    "**": ["search-field.html", "home-sidebar.html"],
}

html_context = {
    # Required for "Edit on GitHub" button
    "github_user": "your-org",             # <-- change
    "github_repo": "dexsuite",             # <-- change
    "github_version": "main",              # branch
    "doc_path": "",                        # docs live at repo root
}

# Copy-button: strip prompts
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True
