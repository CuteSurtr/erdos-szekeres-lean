#!/bin/bash
# Convention A (F2/s2 pipeline.sh steps, with conva_fix.py between build32 and the saturation tests).
# usage: conva.sh SCRATCH OUTDIR in.jsonl
set -e
S=$1; O=$2; shift 2; P=/usr/bin/python3
D=$(cd "$(dirname "$0")/../../F2/s2/scripts" && pwd); H=$(cd "$(dirname "$0")" && pwd)
mkdir -p $O
$P $D/post26.py $O/sets26.jsonl $S/signs26.txt "$@" > $O/post26.log
$S/brute26 26 5 7 7 < $S/signs26.txt > $O/brute26.txt
rm -f $S/sets32.jsonl $O/sat32.jsonl
$P $D/build32.py $O/sets26.jsonl $S/sets32.jsonl > $O/build32.log
$P $H/conva_fix.py $S/sets32.jsonl $S/sets32f.jsonl > $O/conva_fix.log
$P -c "
import json
with open('$O/sets32.jsonl','w') as f:
    for l in open('$S/sets32f.jsonl'):
        f.write(l)"
$P $D/saturate32.py $S/sat $S/ext_solve $S/b33.cnf $O/sets32.jsonl $O/sat32.jsonl 0 lucky=0 > $O/sat32.log
$P -c "
import json,itertools
def o(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
f=open('$S/signs32.txt','w')
for l in open('$S/sets32f.jsonl'):
    r=json.loads(l)
    for key in ('points_exact','points'):
        Q=sorted(map(tuple,r[key])); f.write(''.join('+' if o(Q[i],Q[j],Q[k])>0 else '-' for i,j,k in itertools.combinations(range(len(Q)),3))+'\n')"
$S/brute26 32 33 33 7 < $S/signs32.txt > $O/brute32.txt
