#!/bin/bash

# ./src
SRC_DIR=$(dirname "$(realpath "$0")")
# ./
PROJECT_DIR=$(dirname "$SRC_DIR")

PYTHON_SCRIPT="$SRC_DIR/data_generation.py"
ITERATION=$(grep -oP 'iteration\s*=\s*\K\d+' "$PYTHON_SCRIPT")
EXPERIMENT_INDEX_TEMPLATE=$(grep -oP 'experiment_index\s*=\s*"\K[^"]+' "$PYTHON_SCRIPT")
EXPERIMENT_INDEX=$(echo "$EXPERIMENT_INDEX_TEMPLATE" | sed "s/{iteration}/$ITERATION/") . 

# ./results/experiment_index
EXPERIMENT_DIR="$PROJECT_DIR/results/$EXPERIMENT_INDEX/"

LOG_FILE="$EXPERIMENT_DIR$EXPERIMENT_INDEX.log"
PID_FILE="$EXPERIMENT_DIR$EXPERIMENT_INDEX.pid"

# get current conda env name
TARGET_ENV="inv"
CURRENT_CONDA_ENV=$(basename "$CONDA_PREFIX" 2>/dev/null)

if [[ "$CURRENT_CONDA_ENV" == "$TARGET_ENV" ]]; then

    mkdir -p "$EXPERIMENT_DIR"

    # run python script, start data generation
    nohup python "$PYTHON_SCRIPT" > "$LOG_FILE" 2>&1 &

    PYTHON_PID=$!
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    echo "RUN TIME: $CURRENT_TIME - PID: $PYTHON_PID - EXPERIMENT INDEX: $EXPERIMENT_INDEX" > "$PID_FILE"

else
    echo "ERRO: Current Conda Env isn't '$TARGET_ENV', but '$CURRENT_CONDA_ENV'" | tee -a "$LOG_FILE"
    echo "Please use 'conda activate $TARGET_ENV'" | tee -a "$LOG_FILE"
    exit 1
fi
