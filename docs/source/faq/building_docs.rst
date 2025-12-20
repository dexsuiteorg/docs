Building The Docs Locally
=========================

DexSuite uses Sphinx for documentation. The source lives in ``docs/docs/source/``.

Build (Makefile, recommended)
-----------------------------

From the repo root (Linux/macOS):

.. code-block:: bash

   python -m venv .venv-docs
   . .venv-docs/bin/activate
   pip install -r docs/docs/requirements.txt
   make -C docs/docs html

Output goes to ``docs/docs/build/html``.

Viewing locally
~~~~~~~~~~~~~~~

You can open ``docs/docs/build/html/index.html`` directly, but some browsers can be picky
about JavaScript when opening docs from ``file://``.

If navigation feels flaky, serve the folder instead:

.. code-block:: bash

   python -m http.server --directory docs/docs/build/html 8000

Then open ``http://localhost:8000``.

Build (direct sphinx-build)
---------------------------

.. code-block:: bash

   python -m venv .venv-docs
   . .venv-docs/bin/activate
   pip install -r docs/docs/requirements.txt
   sphinx-build -b html docs/docs/source docs/docs/build/html

Output goes to ``docs/docs/build/html``.
