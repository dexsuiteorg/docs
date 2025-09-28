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

# Repo / "Edit on GitHub" button
html_theme_options = {
    "logo": {
        # drop your SVG/PNG into _static and point here (optional for now)
        # "image_light": "dexsuite-logo-light.png",
        # "image_dark": "dexsuite-logo-dark.png",
        "text": "Dexsuite",
    },
    "use_edit_page_button": True,
    "show_prev_next": False,

    # Version switcher (placeholder); provide _static/versions.json later
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "switcher": {
        "json_url": "_static/versions.json",
        "version_match": release,
    },

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
