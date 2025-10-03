.. include:: ../_shared_nav.rst

Installation
============

.. contents:: On this page
   :local:
   :depth: 2

Prerequisites
-------------

- **OS:** Ubuntu **22.04 LTS** or **24.04 LTS**.
- **GPU:** Required for accelerated simulation/rendering.
- **OpenGL (important):** Your system must use the **GPU** for OpenGL; otherwise Genesis will fail to initialize the renderer.
- **Input device:** You need *at least one* of: **Keyboard**, **3Dconnexion SpaceMouse**, or **Manus gloves** to try Dexsuite interactively.

Quick GPU/OpenGL sanity checks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Optional) Install the small utilities:

.. code-block:: bash

   sudo apt update && sudo apt install -y mesa-utils pciutils

Then verify:

.. code-block:: bash

   # 1) NVIDIA driver present?
   nvidia-smi

   # 2) OpenGL is using your GPU (renderer should show your GPU name, NOT "llvmpipe")
   glxinfo | grep -E "OpenGL vendor|OpenGL renderer"

If `OpenGL renderer` shows **llvmpipe** or generic **Mesa** software, your OpenGL is not using the GPU.

.. tip::

   On hybrid laptops, switching to the discrete GPU often fixes this:

   .. code-block:: bash

      sudo prime-select nvidia
      sudo reboot

   On Ubuntu it also helps to export:

   .. code-block:: bash

      export __GLX_VENDOR_LIBRARY_NAME=nvidia

Direct Installation
-------------------

Option A — PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # (optional but recommended) in a fresh virtual environment you favor
   # python -m venv .venv && source .venv/bin/activate
   # or: conda create -n dexsuite python=3.10 -y && conda activate dexsuite
   # pip install --upgrade pip

   pip install dexsuite

Option B — From source (editable install)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # (optional but recommended) in a fresh virtual environment you favor
   # python -m venv .venv && source .venv/bin/activate
   # or: conda create -n dexsuite python=3.10 -y && conda activate dexsuite
   # pip install --upgrade pip

   git clone <REPO_URL> dexsuite
   cd dexsuite

   pip install -e .


Input Devices
-------------

Dexsuite supports multiple input devices. Have at least one of these connected:

- **Keyboard** — Works out of the box. See :doc:`Keyboard Teleoperation <../getting_started/keyboard_teleoperation>`.
- **SpaceMouse (3Dconnexion)** — Plug-and-play on most Ubuntu setups. If needed, install the daemon:

  .. code-block:: bash

     sudo apt install spacenavd
     sudo systemctl enable --now spacenavd

- **Manus gloves** — Install the vendor runtime/driver per Manus documentation and ensure the device is detected by the system.

Verify the Installation
-----------------------

Quick import test:

.. code-block:: bash

   python - << 'PY'
   import sys
   try:
       import dexsuite
       print("Dexsuite import: OK")
       print("Dexsuite version:", getattr(dexsuite, "__version__", "unknown"))
       print("Python:", sys.version.split()[0])
   except Exception as e:
       print("Dexsuite import failed:", e)
       raise
   PY

If OpenGL/GPU is misconfigured you may see renderer initialization errors from Genesis; resolve them using the **Quick GPU/OpenGL sanity checks** above.

Next Step: Run a Simple Demo
----------------------------

If you’ve completed the steps above, you’re ready to test your setup:

- Head to :doc:`Run a Simple Demo <../getting_started/run_a_simple_demo>` to launch your first environment and confirm everything is working.

Troubleshooting
---------------

- **Genesis/OpenGL initialization errors** (e.g., EGL/GLX/llvmpipe):
  - Confirm `nvidia-smi` works and that `glxinfo` reports your **GPU** as the OpenGL renderer.
  - For hybrid laptops: ``sudo prime-select nvidia`` and reboot.
  - Try exporting ``__GLX_VENDOR_LIBRARY_NAME=nvidia`` in your shell before launching Python.

- **Device not detected (SpaceMouse/Manus):**
  - Replug the device and check `dmesg` output.
  - For SpaceMouse, ensure ``spacenavd`` is running.
  - For Manus gloves, confirm the vendor service/app is running and the device is paired.
- **Python version:**
  - Generally speaking, python >= 3.8 should work fine. We recommend python = 3.10.
