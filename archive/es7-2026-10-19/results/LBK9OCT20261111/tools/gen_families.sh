#!/bin/sh
# Generate every added clause family for t layers (m = 8, B = 2) into OUTDIR (no chain clauses).
# usage: gen_families.sh t OUTDIR [PYTHON]
set -e
T=$(cd "$(dirname "$0")" && pwd); t=$1; O=$2; PY=${3:-python3}; mkdir -p $O; cd $O
NV0=$(python3 -c "
import importlib.util,sys
s=importlib.util.spec_from_file_location('gen','$T/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
E,_,_=G.build(8,9,$t,chain=True,body=open('/dev/null','w')); print(E.nv)")
echo $NV0 > nv0.txt
python3 $T/chord_rules_m.py 8 $t chord.clauses > /dev/null
python3 $T/cone_rules.py 8 $t cone.clauses > /dev/null
python3 $T/thr_rules2.py 8 $t thr2.clauses > /dev/null
python3 $T/cell_rules.py 8 $t 2 $NV0 cellB2.clauses > /dev/null
python3 $T/cell_thr.py 8 $t 2 $NV0 thr2.clauses cellthrB2.clauses > /dev/null
python3 $T/binorder.py 8 $t 2 $NV0 binorderB2.clauses
wc -l *.clauses
