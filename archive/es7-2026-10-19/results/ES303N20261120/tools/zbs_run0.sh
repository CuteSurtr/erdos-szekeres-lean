#!/bin/bash
# Balanced budget-B tree on catalog + Z-row + Z*-row (v4, 20 Nov), ZERO SIDE ONLY (state 0 occupied), for ExcludesHoleBudgetZZsF B
# (zrow/leanzs/BalancedBudgetsZZs.lean; h_0 = h_1 = 0 justified by FixedStatesZ).
# fastbb256 (finder only; it fixes state 0 occupied itself) -> balz_assemble_v4.py with MIS "-" (assembly + check_tree
# replay of every file; the pending side "0 missing" of the first branch is the only pending leaf of each file)
# -> balcheck2 (own C++) with the Z-row and the lemma path "0:1" in the cover check.
# Resumable: rerun with the same arguments; fastbb256 resumes from its closed contexts (occ.out is appended).
# usage: zb_run0.sh B THREADS CONTEXTS
set -u
B=$1; T=$2; C=$3; D=/home/jay/research/data/bal186-20261119/zrow; cd $D; O=$D/b${B}zs; mkdir -p $O
CAT=/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
FB=$D/../fastbb256; FL="--ktop=16 --klow=4 --dtop=0 --dmid=0 --on-witness=stop --max-ctx-nodes=5000000 --time-limit=259200"
log() { echo "$(date '+%F %T') $*" >> $O/steps.log; }
log "start B=$B T=$T C=$C (zero side only, Z*-row)"
$FB solve balzs.rows $B $T $C $O/occ $FL >> $O/occ.out 2>&1; rc=$?; log "occ (0 occupied) rc=$rc"; [ $rc -eq 0 ] || exit $rc
python3 -I balz_assemble_v4.py $B $O/occ - $O/files $T > $O/assemble.out 2>&1; rc=$?; log "assemble+check_tree rc=$rc $(tail -c 600 $O/assemble.out)"
K=$(ls $O/files/ctx-*-zb$B.json.gz | wc -l)
BALCHECK_EXTRA_ROWS=$D/zzs_rows.json BALCHECK_LEMMA_PATHS="0:1" ../balcheck/balcheck2 $CAT $B $K $T "$O/files/ctx-%d-zb$B.json.gz" $O/balcheck.tsv > $O/balcheck.json 2> $O/balcheck.err; rc2=$?
log "balcheck2 rc=$rc2 $(cat $O/balcheck.json)"
exit $(( rc | rc2 ))
