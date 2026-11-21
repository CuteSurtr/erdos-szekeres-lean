#!/bin/bash
# balanced budget-B tree on catalog + Z-row (ES306N20261119 §9): both state-0 sides with fastbb256 (finder only),
# assembly + check_tree replay of every file (balz_assemble.py), then the independent checker balcheck with the Z-row.
set -u
B=$1; T=$2; C=$3; D=/home/jay/research/data/bal186-20261119/zrow; cd $D; O=$D/b$B; mkdir -p $O
CAT=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
FB=$D/../fastbb256; FL="--ktop=16 --klow=4 --dtop=0 --dmid=0 --on-witness=stop --max-ctx-nodes=5000000 --time-limit=86400"
log() { echo "$(date '+%F %T') $*" >> $O/steps.log; }
log "start B=$B T=$T C=$C"
$FB solve balz.rows $B $T $C $O/occ $FL > $O/occ.out 2>&1; rc=$?; log "occ (0 occupied) rc=$rc"; [ $rc -eq 0 ] || exit $rc
$FB solve balz_m0.rows $((B-1)) $T $C $O/mis $FL > $O/mis.out 2>&1; rc=$?; log "mis (0 missing) rc=$rc"; [ $rc -eq 0 ] || exit $rc
python3 -I balz_assemble.py $B $O/occ $O/mis $O/files $T > $O/assemble.out 2>&1; rc=$?; log "assemble+check_tree rc=$rc $(tail -c 600 $O/assemble.out)"
K=$(ls $O/files/ctx-*-zb$B.json.gz | wc -l)
BALCHECK_EXTRA_ROWS=$D/zrow.json ../balcheck/balcheck $CAT $B $K $T "$O/files/ctx-%d-zb$B.json.gz" $O/balcheck.tsv > $O/balcheck.json 2> $O/balcheck.err; rc2=$?
log "balcheck rc=$rc2 $(cat $O/balcheck.json)"
exit $(( rc | rc2 ))
