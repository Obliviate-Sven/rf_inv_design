#!/bin/bash

end_time=$(date -d "2025-03-30 00:00:00" +%s)

while [ $(date +%s) -lt $end_time ]; do

    rm core.*

    running_copies=$(ps aux | grep '[p]ython.*/copy[0-9]\{2\}/' | grep -oP 'copy\d{2}' | awk -F 'copy' '{print $2}' | sort -u)

    all_copies=$(seq -w 0 19)

    missing=()
    for copy in $all_copies; do
        if ! echo "$running_copies" | grep -q "^$copy$"; then
            missing+=("$copy")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        echo "${missing[@]} dumped"
        for copy in "${missing[@]}"; do
            script_path="/data/inverse_design/experiments/copy${copy}/src/run.sh"
            if [ -f "$script_path" ]; then
                echo "rebooting ${copy}"
		bash "./killall.sh"
		bash "./run_all.sh"
               #  bash "$script_path"

            else
                echo "warning: ${script_path} doesn't exist"
            fi
        done
    else
        echo "all fine"
    fi

    sleep 30
done

echo "Monitor exited"
