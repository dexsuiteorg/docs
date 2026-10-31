#!/bin/bash
# Export every documented task at reset for the docs renders (<docs_work>/docs_tasks/<task>/scene.json). GPU from $GPU.
#   tools/export_tasks.sh lift=franka:allegro spray_graffiti=floating:sharpa ...
# PYTHON: a Python with DexSuite's dependencies; paths as in tools/paths.py (DEXSUITE_DOCS_WORK, DEXSUITE_REPO).
cd "$(dirname "$0")/.."
PY=${PYTHON:-python}
WORK=${DEXSUITE_DOCS_WORK:-$(cd .. && pwd)/docs_work}/docs_tasks
mkdir -p "$WORK/_logs"
export CUDA_VISIBLE_DEVICES=${GPU:-0} EGL_DEVICE_ID=${GPU:-0} PYOPENGL_PLATFORM=egl
for spec in "$@"; do
  task=${spec%%=*}; robot=${spec#*=}
  [ -f "$WORK/$task/scene.json" ] && { echo "skip $task"; continue; }
  timeout 900 "$PY" tools/export_task_scene.py --task "$task" --robot "$robot" --out "$WORK/$task" > "$WORK/_logs/$task.log" 2>&1 \
    && grep "^ok" "$WORK/_logs/$task.log" || { echo "FAILED $task"; tail -3 "$WORK/_logs/$task.log"; }
done
echo done
