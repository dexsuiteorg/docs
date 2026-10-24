#!/bin/bash
# Export every documented task at reset for the docs renders (runs/docs_tasks/<task>/scene.json). GPU from $GPU.
cd /efs/projects/fudi
export CUDA_VISIBLE_DEVICES=${GPU:-0} EGL_DEVICE_ID=${GPU:-0} PYOPENGL_PLATFORM=egl
for spec in "$@"; do
  task=${spec%%=*}; robot=${spec#*=}
  [ -f runs/docs_tasks/$task/scene.json ] && { echo "skip $task"; continue; }
  timeout 900 .venv-dexsuite/bin/python dexsuite_docs/tools/export_task_scene.py --task $task --robot $robot --out runs/docs_tasks/$task > runs/docs_tasks/_logs/$task.log 2>&1 \
    && grep "^ok" runs/docs_tasks/_logs/$task.log || { echo "FAILED $task"; tail -3 runs/docs_tasks/_logs/$task.log; }
done
echo done
