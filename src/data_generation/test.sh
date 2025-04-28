#!/bin/bash

# ./src
SRC_DIR=$(dirname "$(realpath "$0")")
# ./
PROJECT_DIR=$(dirname "$SRC_DIR")

PYTHON_SCRIPT="$SRC_DIR/data_generation.py"
ITERATION=$(grep -oP 'iteration\s*=\s*\K\d+' "$PYTHON_SCRIPT")
EXPERIMENT_INDEX_TEMPLATE=$(grep -oP 'experiment_index\s*=\s*"\K[^"]+' "$PYTHON_SCRIPT")
EXPERIMENT_INDEX=$(echo "$EXPERIMENT_INDEX_TEMPLATE" | sed "s/{iteration}/$ITERATION/")
echo "$EXPERIMENT_INDEX"