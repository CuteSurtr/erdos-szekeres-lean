#!/bin/sh
# Rebuild the base formula of Theorem 1 (MODE=mono, S8.cnf), Theorem 2 (MODE=mono2to14, S13.cnf) or of a window a..b
# (MODE=a-b, e.g. 3-13 for S14.cnf, 1-12 for V1.cnf, 4-15 for V4.cnf) from the generators.
# usage: build_base.sh OUTDIR MODE   (writes OUTDIR/BASE.cnf and prints SHA-256 of every part)
set -e
T=$(cd "$(dirname "$0")" && pwd); O=$1; MODE=${2:-mono}; mkdir -p $O; cd $O
python3 $T/gen.py 8 9 16 A16.cnf > gen.log
python3 $T/chord_rules_m.py 8 16 chord.clauses
python3 $T/cone_rules.py 8 16 cone.clauses
python3 $T/thr_rules2.py 8 16 thr2.clauses
python3 $T/cell_rules.py 8 16 2 497697 cellB2.clauses
python3 $T/cell_thr.py 8 16 2 497697 thr2.clauses cellthrB2.clauses
python3 $T/binorder.py 8 16 2 497697 binorder.clauses
python3 -c "
import json, sys; d=json.load(open('A16.cnf.json')); mode=sys.argv[1]
lo,hi=(1,15) if mode=='mono' else ((2,14) if mode=='mono2to14' else tuple(map(int,mode.split('-'))))
ok=lambda i,j: i>=lo and j<=hi
open('mono.units','w').write(''.join('%d 0\n' % v for k,v in d['Y'].items() if ok(*map(int,k.split(',')))))" $MODE
cat chord.clauses cone.clauses thr2.clauses cellB2.clauses cellthrB2.clauses binorder.clauses mono.units > extra.txt
read -r p c nv ncl < A16.cnf
ne=$(wc -l < extra.txt)
{ echo "p cnf $((nv + 15)) $((ncl + ne))"; tail -n +2 A16.cnf; cat extra.txt; } > BASE.cnf
sha256sum A16.cnf chord.clauses cone.clauses thr2.clauses cellB2.clauses cellthrB2.clauses binorder.clauses mono.units BASE.cnf
