#!/bin/bash

TARGET_DIR="/data/inverse_design/results/3.15_8000_iter_result"

mkdir -p "$TARGET_DIR"

find . -name "*data.csv" | while read filepath; do

  filename=$(basename "$filepath")

  parentdir=$(basename "$(dirname "$(dirname "$(dirname "$filepath")")")")

  newname="${parentdir}_${filename}"

  cp "$filepath" "${TARGET_DIR}/${newname}"

  echo "Copied: $filepath --> ${TARGET_DIR}/${newname}"
done
