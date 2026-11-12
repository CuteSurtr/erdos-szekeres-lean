#!/bin/sh
# Exact controls (cheap part): label the exact sets, evaluate every non-chain clause family on them.
# usage: run_controls.sh RESULTS_DIR   (writes to stdout)
R=$1; T=$(cd "$(dirname "$0")" && pwd); W=$(cd "$T/.." && pwd)
for f in PRIMEFOLD/sets/k9/c8_120pts_15layers K9SEARCH/sets/f_del0 PRIMEFOLD/sets2/c8_120pts_blowup2orb PRIMEFOLD/sets2/c8_120pts_blowup3orb; do
  b=$(basename $f); echo "== $b"; sha256sum $R/$f.pts | cut -c1-16
  python3 $T/label8.py $R/$f.pts $W/ctrl/$b.json
  python3 $T/check_cnf.py $W/ctrl/$b.json $W/cnf/A_m8K9t15.cnf $W/cnf/chord_m8t15.clauses $W/cnf/cone_m8t15.clauses $W/cnf/thr2_m8t15.clauses --units $W/ctrl/$b.units
  python3 $T/check_cells.py $R/$f.pts 410352 $W/univ/cell_B2_t15.clauses $W/univ/cellthr_B2_t15.clauses
done
f=K9SEARCH/sets/k9_128_final; b=k9_128_final; echo "== $b"; sha256sum $R/$f.pts | cut -c1-16
python3 $T/label8.py $R/$f.pts $W/ctrl/$b.json
python3 $T/check_cnf.py $W/ctrl/$b.json $W/cnf/A_m8K9t16.cnf $W/cnf/chord_m8t16.clauses $W/cnf/cone_m8t16.clauses $W/cnf/thr2_m8t16.clauses --units $W/ctrl/$b.units
python3 $T/check_cells.py $R/$f.pts 497697 $W/cnf/cellB2_m8t16.clauses $W/cnf/cellthrB2_m8t16.clauses
