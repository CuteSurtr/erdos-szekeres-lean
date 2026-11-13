#!/bin/bash
# certificate attempt for 19 holes: cubes with LRAT over all current rows, then justify the used rows.
set -e
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
OD=final19
$PY dump_all.py $OD/rows_final.json
$PY -u cube_lrat.py $OD/rows_final.json 18 $OD/cubes_final 5 22,37,45,53,67
cp $OD/cubes_final/used_rows.json $OD/subset19_rows.json
$PY -u static_check.py 17 18
PAR_SIGMA=1 $PY -u template_cert2.py $OD/subset19_rows.json $OD/tcert 5
$PY -u pb_consistency.py $OD/rows_final.json 18
$PY -u final_verify.py $OD/tcert
echo FINAL19B_DONE
