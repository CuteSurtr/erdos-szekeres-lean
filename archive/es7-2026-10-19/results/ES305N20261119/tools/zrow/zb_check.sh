#!/bin/bash
# assembly + check_tree replay + balcheck for an existing budget-B Z-row packet pair (both fastbb sides done)
set -u
B=$1; T=$2; D=/home/jay/research/data/bal186-20261119/zrow; cd $D; O=$D/b$B
CAT=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
log() { echo "$(date '+%F %T') $*" >> $O/steps.log; }
python3 -I balz_assemble.py $B $O/occ $O/mis $O/files $T > $O/assemble.out 2>&1; rc=$?; log "assemble+check_tree rc=$rc $(tail -c 600 $O/assemble.out)"
K=$(ls $O/files/ctx-*-zb$B.json.gz | wc -l)
BALCHECK_EXTRA_ROWS=$D/zrow.json ../balcheck/balcheck $CAT $B $K $T "$O/files/ctx-%d-zb$B.json.gz" $O/balcheck.tsv > $O/balcheck.json 2> $O/balcheck.err; rc2=$?
log "balcheck rc=$rc2 $(cat $O/balcheck.json)"
exit $(( rc | rc2 ))
