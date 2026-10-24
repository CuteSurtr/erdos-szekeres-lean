#!/bin/bash
# FIX1 part 1: run aggregate_final_v2.py (and the old script, for comparison) on the inputs of
# results/V3Z/aggregate_inputs.txt; F and M.jsonl rebuilt as results/V3Z/tools.txt and inputs.txt say.
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
cd $R
FILES=$(cat results/V3Z/aggregate_inputs.txt)
python3 results/FIX1/aggregate_final_v2.py $R /opt/work/F.cnf /opt/work/M.jsonl results/FIX1/agg/accepted_v2.tsv $FILES > results/FIX1/agg/problems_v2.txt
cmp results/FIX1/agg/accepted_v2.tsv results/V3Z/accepted_final.tsv && echo "v2 tsv identical to V3Z accepted_final.tsv"
python3 results/FIX1/scripts/mutate_agg.py $R /opt/work/F.cnf /opt/work/M.jsonl /opt/work/mut $FILES > results/FIX1/agg/mutation.txt
