#!/bin/sh
# Rebuild S8.cnf (monotone cube base) and the c_r cube formulas' hashes from the generators.
# usage: build_S8.sh OUTDIR [PYTHON_WITH_NUMPY]   (writes OUTDIR/S8.cnf and prints SHA-256 of every part)
set -e
T=$(cd "$(dirname "$0")" && pwd); O=$1; PY=${2:-python3}; mkdir -p $O; cd $O
python3 $T/gen.py 8 9 16 A16.cnf > gen.log
python3 $T/chord_rules_m.py 8 16 chord.clauses
python3 $T/cone_rules.py 8 16 cone.clauses
python3 $T/thr_rules2.py 8 16 thr2.clauses
python3 $T/cell_rules.py 8 16 2 497697 cellB2.clauses
python3 $T/cell_thr.py 8 16 2 497697 thr2.clauses cellthrB2.clauses
python3 $T/binorder.py 8 16 2 497697 binorder.clauses
python3 -c "
import json; d=json.load(open('A16.cnf.json'))
open('mono.units','w').write(''.join('%d 0\n' % v for v in d['Y'].values()))"
cat chord.clauses cone.clauses thr2.clauses cellB2.clauses cellthrB2.clauses binorder.clauses mono.units > extra.txt
read -r p c nv ncl < A16.cnf
ne=$(wc -l < extra.txt)
{ echo "p cnf $((nv + 15)) $((ncl + ne))"; tail -n +2 A16.cnf; cat extra.txt; } > S8.cnf
sha256sum A16.cnf chord.clauses cone.clauses thr2.clauses cellB2.clauses cellthrB2.clauses binorder.clauses mono.units S8.cnf
