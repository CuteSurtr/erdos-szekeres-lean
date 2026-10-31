#!/bin/bash
# run aggregate_final.py over M.jsonl with every leaf/cover record file of V3T, V3A..V3E, V3Z
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
cd $R
FILES=$(for f in $(find results/V3T results/V3A results/V3B results/V3C results/V3D results/V3E results/V3Z -name '*.jsonl' | sort); do grep -q '"kind"' $f && echo $f; done)
echo "$FILES" > /opt/work/agg_files.txt
time python3 $R/results/V3Z/scripts/aggregate_final.py $R /opt/work/F.cnf /opt/work/M.jsonl $R/results/V3Z/accepted_final.tsv $FILES > $R/results/V3Z/problems.txt
