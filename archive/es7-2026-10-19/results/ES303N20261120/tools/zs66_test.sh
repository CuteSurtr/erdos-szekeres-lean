#!/bin/bash
# Pipeline test of the v4 assembly + check_tree replay + balcheck2 (two extra rows) on the budget-66 Z*-row tree.
D=/home/jay/research/data/bal186-20261119/zrow; cd $D; O=$D/zs66; B=66
CAT=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
python3 -I balz_assemble_v4.py $B $O/occ - $O/files 1 > $O/assemble.out 2>&1; echo "assemble rc=$?"
K=$(ls $O/files/ctx-*-zb$B.json.gz | wc -l); echo "files $K"
BALCHECK_EXTRA_ROWS=$D/zzs_rows.json BALCHECK_LEMMA_PATHS="0:1" ../balcheck/balcheck2 $CAT $B $K 1 "$O/files/ctx-%d-zb$B.json.gz" $O/balcheck.tsv > $O/balcheck.json 2> $O/balcheck.err; echo "balcheck2 rc=$?"
