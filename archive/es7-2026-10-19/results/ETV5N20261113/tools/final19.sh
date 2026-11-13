#!/bin/bash
set -e
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
OD=final19
cp $OD/cubes_all/used_rows.json $OD/subset19_rows.json
$PY -u static_check.py 17 18 19
PAR_SIGMA=1 $PY -u template_cert2.py $OD/subset19_rows.json $OD/tcert 5
$PY -u cube_lrat.py $OD/subset19_rows.json 18 $OD/cubes_sub 5 22,37,45,53,67
$PY -u pb_consistency.py $OD/subset19_rows.json 18
$PY -u final_verify.py $OD/tcert
echo FINAL19_DONE
