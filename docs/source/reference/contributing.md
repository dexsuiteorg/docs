# Contributing

<p class="ds-lede">New tasks, robots, sensors and fixes are welcome. Every task added to DexSuite runs with every arm
and end-effector that fits it, so one contribution is useful to everyone.</p>

## Code

1. Fork the repository and create a branch.
2. Add your task, robot or sensor following the [how-to guides](../how-to/index.md).
3. Run the tests from the repository root:

   ```bash
   pytest tests -m "not slow"
   ```

   The suite builds robots and environments, checks cameras, workspaces, controllers and the LeRobot round trip.
   Tests marked `slow` build every robot.
4. Open a pull request with a short description and, for a new task or robot, a screenshot from the viewer.

## These docs

The documentation lives in its own repository, [dexsuiteorg/docs](https://github.com/dexsuiteorg/docs), as Markdown
(MyST) under `docs/source`, built with Sphinx and the PyData theme, and published by Read the Docs.

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs/source docs/_build/html
python -m http.server --bind 127.0.0.1 -d docs/_build/html 8000      # open http://localhost:8000
```

Generated pages and assets come from the scripts in `tools/`. Re-run them after the code changes:

| Script | Produces |
|---|---|
| `tools/catalog_data.py` | the facts behind the task and robot pages (edit this) |
| `tools/build_catalog.py` | `tasks/*.md`, `robots/*.md`, the dataset and results tables |
| `tools/gen_reference.py` | `reference/options.md`, `reference/registry.md`, from the DexSuite source |
| `tools/check_tasks.py` | runs every task page's snippet and records what it returns |
| `tools/export_task_scene.py`, `tools/render_tasks.py` | the task renders (Genesis export, Blender Cycles) |
| `tools/render_catalog.py` | the arm and end-effector renders |
| `tools/make_diagrams.py` | the concept diagrams |
| `tools/make_wordmark.py` | the DexSuite wordmark |

Renders are made with Blender Cycles from exports of the real DexSuite scenes, on transparent backgrounds, with the
same lights as the [project page](https://dexsuiteorg.github.io/).
