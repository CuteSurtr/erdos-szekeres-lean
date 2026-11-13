#!/bin/bash
# self-contained re-proof of the 19-hole arithmetic over the justified subset only
set -e
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
OD=final19
$PY -u cube_lrat.py $OD/subset19_rows.json 18 $OD/cubes_sub 5 22,37,45,53,67
$PY -u pb_consistency.py $OD/subset19_rows.json 18
echo FINAL19C_DONE
