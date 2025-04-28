#! /bin/bash

find ./ -type f -name "run.sh" -exec bash -c '
    chmod +x "$1"        
    bash "$1"
' _ {} \;