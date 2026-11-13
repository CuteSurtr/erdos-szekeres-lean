#!/bin/bash
# phase 2/3 for budget 17 (target 18 holes): justify the used rows, then a self-contained cube certificate over them.
set -e
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
OD=final18
cp $OD/cubes_all/used_rows.json $OD/subset18_rows.json
$PY -u template_cert.py $OD/subset18_rows.json $OD/tcert 4
$PY -u cube_lrat.py $OD/subset18_rows.json 17 $OD/cubes_sub 4 22,37,45,53,67
$PY -u pb_consistency.py $OD/subset18_rows.json 17
$PY -u final_verify.py $OD/tcert
echo FINAL18_DONE
