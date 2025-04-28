#!/bin/bash

# ./src
SRC_DIR=$(dirname "$(realpath "$0")")
# ./
PROJECT_DIR=$(dirname "$SRC_DIR")
ROOT_DIR=$(dirname "$PROJECT_DIR")

PYTHON_SCRIPT="$SRC_DIR/data_generation.py"
EXPERIMENT_INDEX=$(grep -oP 'experiment_index\s*=\s*"\K[^"]+' $PYTHON_SCRIPT)

# ./results/experiment_index
EXPERIMENT_DIR="$PROJECT_DIR/results/$EXPERIMENT_INDEX/"

LOG_FILE="$EXPERIMENT_DIR$EXPERIMENT_INDEX.log"
PID_FILE="$EXPERIMENT_DIR$EXPERIMENT_INDEX.pid"

rm "$SRC_DIR"/*.log
rm -rf "$PROJECT_DIR"/tmp/
rm -r "$PROJECT_DIR"_"$EXPERIMENT_INDEX"*
rm -r "$EXPERIMENT_DIR"