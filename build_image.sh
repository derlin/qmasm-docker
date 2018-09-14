#!/bin/bash

if [[ "$1" = "-d" ]]; then
    # dry run
    echo "The command is:"
    echo "docker build -t qmasm-rest --rm `dirname "$0"`"
else
    # actually build the image
    docker build -t qmasm-rest --rm `dirname "$0"`
fi
