#!/bin/bash
# End-to-end processing of realized 26-point sets.
# usage: pipeline.sh SCRATCH OUTDIR armF_*.jsonl
# needs in SCRATCH: brute26, sat (tools/trackA/sat.c), ext_solve (results/A/scripts/ext_solve.cpp), b33.cnf (gen_cnf.py 33 7)
set -e
S=$1; O=$2; shift 2
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p $O
/usr/bin/python3 $D/post26.py $O/sets26.jsonl $S/signs26.txt "$@" > $O/post26.log
$S/brute26 26 5 7 7 < $S/signs26.txt > $O/brute26.txt
/usr/bin/python3 $D/build32.py $O/sets26.jsonl $S/sets32.jsonl >> $O/build32.log
/usr/bin/python3 -c "
import json,sys
with open('$O/sets32.jsonl','w') as f:
    for l in open('$S/sets32.jsonl'):
        f.write(l)"
/usr/bin/python3 $D/saturate32.py $S/sat $S/ext_solve $S/b33.cnf $O/sets32.jsonl $O/sat32.jsonl 0 lucky=0 >> $O/sat32.log
# brute-force: every 32-set (exact and compressed), x-sorted signs, no convex 7-subset (cap/cup limits off)
/usr/bin/python3 -c "
import json,itertools
def o(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
f=open('$S/signs32.txt','w')
for l in open('$S/sets32.jsonl'):
    r=json.loads(l)
    for key in [k for k in ('points_exact','points') if k in r]:
        Q=sorted(map(tuple,r[key])); f.write(''.join('+' if o(Q[i],Q[j],Q[k])>0 else '-' for i,j,k in itertools.combinations(range(len(Q)),3))+'\n')"
$S/brute26 32 33 33 7 < $S/signs32.txt > $O/brute32.txt
