Installation
============

.. contents:: On this page
   :local:
   :depth: 2

System Requirements
-------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Requirement
     - Specification
   * - Python
     - 3.10 or later
   * - Physics Engine
     - Genesis 0.3.3, installed automatically


Verify GPU and OpenGL
---------------------


Genesis can use OpenGL to accelerate the rendering process. If you plan to use it, verify your setup before installing.

Install these command-line tools to help check your system, if you don't already have them:

.. code-block:: bash

   sudo apt update && sudo apt install -y mesa-utils pciutils

Run the checks:

.. code-block:: bash

   # Confirm the NVIDIA driver is loaded
   nvidia-smi

   # Confirm OpenGL is using the GPU
   # The renderer line must show your GPU name, NOT "llvmpipe" or "softpipe"
   glxinfo | grep -E "OpenGL vendor|OpenGL renderer"

.. note::

   On hybrid laptops (Intel + NVIDIA), OpenGL may default to the integrated GPU or to software rendering. Switch to the discrete GPU before proceeding:

   .. code-block:: bash

      sudo prime-select nvidia
      sudo reboot

   If the issue persists after rebooting, add the following line to your shell profile:

   .. code-block:: bash

      export __GLX_VENDOR_LIBRARY_NAME=nvidia

Install DexSuite
----------------

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We highly recommend installing DexSuite inside a virtual environment. 
This prevents it from conflicting with other Python projects on your computer.

Using ``venv``:

.. code-block:: bash

   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip

Using ``conda``:

.. code-block:: bash

   conda create -n dexsuite python=3.10 -y
   conda activate dexsuite
   pip install --upgrade pip



Installing From Source
~~~~~~~~~~~~~~~~~~~~~


.. code-block:: bash

   git clone <REPO_URL> dexsuite
   cd dexsuite
   pip install -e .



Verify the Installation
-----------------------

Run the following to confirm that DexSuite imports correctly:

.. code-block:: bash

   python - << 'PY'
   import sys, dexsuite
   print("Python    :", sys.version.split()[0])
   print("DexSuite  :", getattr(dexsuite, "__version__", "unknown"))
   print("Status    : OK")
   PY

Expected output:

.. code-block:: text

   Python    : 3.10.x
   DexSuite  : 0.1.3
   Status    : OK

Troubleshooting
---------------

**Genesis is running very slowly or shows EGL/GLX errors**

OpenGL is not reaching the GPU. Repeat the GPU verification steps above. On hybrid laptops, run ``sudo prime-select nvidia`` and reboot. If the problem persists, add ``export __GLX_VENDOR_LIBRARY_NAME=nvidia`` to your shell profile and open a new terminal.


**OpenGL errors inside a Virtual Machine (VM)**

For machines with Nvidia GPU, try to force GPU-accelerated rendering by exporting the following environment variables inside the Ubuntu VM:

.. code-block:: bash

  export LIBGL_ALWAYS_INDIRECT=0
  export GALLIUM_DRIVER=d3d12
  export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA


If it does not work, try installing the latest version of OSMesa:

.. code-block:: bash
  sudo add-apt-repository ppa:kisak/kisak-mesa
  sudo apt update
  sudo apt upgrade

Then, only enforce direct rendering:

.. code-block:: bash

  export LIBGL_ALWAYS_INDIRECT=0


At the point, `glxinfo` mesa utility can be used to determine which OpenGL vendor is being used by default, i.e.:

.. code-block:: bash

  glxinfo -B


As a last resort, one can force CPU (aka. software) rendering using OSMesa if necessary as follows:

.. code-block:: bash

  export LIBGL_ALWAYS_SOFTWARE=1


**Python version is below 3.10**

Check which interpreter is active:

.. code-block:: bash

   python --version

Recreate the virtual environment with a supported interpreter if the version is below 3.10.

Next Steps
----------

Continue to :doc:`run_a_simple_demo` to launch your first environment and verify the full stack.
