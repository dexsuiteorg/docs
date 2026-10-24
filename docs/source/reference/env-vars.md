# Environment variables

<p class="ds-lede">DexSuite reads a few environment variables. None is required.</p>

| Variable | Effect |
|---|---|
| `PYOPENGL_PLATFORM=egl` | Render cameras offscreen on a machine without a display. Set it before importing DexSuite. |
| `DEXSUITE_<NAME>_DIR` | Use another folder for an asset category, for example `DEXSUITE_OBJECTS_DIR`. |
| `DEXSUITE_MJCF_CACHE_DIR` | Where processed model files are cached. Default: `$TMPDIR/dexsuite_mjcf`. |
| `DEXSUITE_STATUS=0` | Turn off the console status display. |
| `DEXSUITE_SPINNER=0` | Turn off the console spinner. |
| `DEXSUITE_TOASTER_SLOT` | Slot geometry of the [Toast Bread](../tasks/put_bread_toaster.md) toaster. Default: `wide_b`. |

The compute device is chosen in code with `ds.set_device("cuda:1")` before the first `ds.make`, and
`ds.get_device()` returns it.
