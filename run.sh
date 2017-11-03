#!/bin/bash

ROOT=$(cd $(dirname $0) && pwd)

### Python ###
python $ROOT/python/src/main.py "$@"
