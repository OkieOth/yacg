#!/bin/sh

if ! [ -z "$BREAKPOINT" ]; then
    BREAKPOINT_IMPL="--breakpoint $BREAKPOINT"
fi

python3 -m debugpy --listen 0.0.0.0:5678 ${BREAKPOINT_IMPL} --wait-for-client yacg.py "$@"