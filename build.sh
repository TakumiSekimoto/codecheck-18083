#!/bin/bash

ROOT=$(cd $(dirname $0) && pwd)

### Python ###
cd $ROOT/python/src
python -m compileall .