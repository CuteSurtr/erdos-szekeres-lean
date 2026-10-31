#!/bin/bash
# For one realized 26-point set NAME.pts: exact verify26 (F2), fingerprint vs F2 (and earlier F6 sets),
# copy to data/sets26, then process_new.sh in a private scratch dir (both 32-point conventions).
# usage: handle26.sh SCRATCH PTS
S=$1; P=$2; N=$(basename $P .pts)
R=$(cd "$(dirname "$0")/../.." && pwd); PY=/usr/bin/python3; D=$R/F6/data/sets26
mkdir -p $D; cp $P $D/$N.pts
$PY $R/F2/scripts/verify26.py $S/brute $D/$N.pts > $D/$N.verify26.json
$PY $R/F6/scripts/fingerprint26.py $D/$N.fp.json $(ls $D/*.pts | grep -v "/$N.pts") $D/$N.pts > /dev/null
W=$S/proc/$N; mkdir -p $W/tools
for t in sat ext_solve brute_kgon brute26 b33.cnf; do ln -sf $S/$t $W/tools/$t; done
$PY - $D/$N.pts $W/in.jsonl $N <<'PYEOF'
import json, itertools, sys
def o(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
P = sorted(tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip())
m = ''.join('+' if o(P[i],P[j],P[k]) > 0 else '-' for i,j,k in itertools.combinations(range(len(P)),3))
open(sys.argv[2],'w').write(json.dumps({'id': sys.argv[3], 'points': [list(p) for p in P], 'model': m}) + '\n')
PYEOF
bash $R/F6/scripts/process_new.sh $W/tools $W/out $W/in.jsonl > $W/process.log 2>&1
echo "DONE $N rc=$?"
