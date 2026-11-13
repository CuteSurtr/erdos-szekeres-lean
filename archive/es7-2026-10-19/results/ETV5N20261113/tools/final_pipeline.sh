#!/bin/bash
# usage: final_pipeline.sh <budget (= target holes - 1)> <outdir> <procs>
set -e
B=$1; OD=$2; NP=$3; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
mkdir -p $OD
$PY dump_all.py $OD/rows_all.json
$PY -u pb_lrat.py $OD/rows_all.json $B $OD/pb_all
cp $OD/pb_all/used_rows.json $OD/subset_rows.json
$PY -u template_cert.py $OD/subset_rows.json $OD/tcert $NP
$PY -u pb_lrat.py $OD/subset_rows.json $B $OD/pb_sub
$PY -u final_verify.py $OD/tcert
echo PIPELINE_DONE
