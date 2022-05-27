#!/bin/bash
echo $(pwd)
set -x
# not sure why but the output here isn't writing to the command line without cat
# and that breaks the reporter as well
coverage run -m pytest -q | cat
coverage report -m --skip-covered
coverage html
