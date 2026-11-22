#!/bin/bash
# The reviewer's ONE Lean compile (inside unit esr-ag-rv5-axioms): bare v4.24.0 lean, no -o (no olean written).
V=/home/jay/research/data/formalize-20261122/n66-l15-rows/review
source $V/env.sh
cd $V
{ echo "== $(date '+%F %T') sha256 $(sha256sum ReviewL15R.lean | cut -d' ' -f1)"; echo "LEAN_PATH=$LEAN_PATH";
  /usr/bin/time -v $TC/bin/lean -j1 ReviewL15R.lean; echo "lean_rc=$?"; echo "== $(date '+%F %T') end"; } > $V/review_compile.log 2>&1
grep -q '^lean_rc=0$' $V/review_compile.log
