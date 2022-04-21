#!/bin/bash

docker run -it -v $(pwd):/app/ -p8050:8050 python-dash bash -c "$@"
