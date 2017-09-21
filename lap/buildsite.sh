#!/bin/sh

if [ "$@" ]; then
    AST=pop
else
    AST=DEVEL
fi

PYTHONPATH=/home/users/lap_www/lib ATLASSITE_TARGET=$AST python scripts/buildsite.py "$@"

