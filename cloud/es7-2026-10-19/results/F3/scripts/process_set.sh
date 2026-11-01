#!/bin/bash
# Process one realized 26-point set S.pts (integer 'x y' lines):
#  1. exact checks: F2 verify26.py (general position, cap/cup, largest convex subset, brute.c) and
#     F2/s2 post26.py + brute26.c (inside pipeline.sh);
#  2. canonical order-type fingerprint (fingerprint.py) vs KNOWN (F2 sets and earlier F3 sets);
#     duplicates stop here;
#  3. convention A (conva.sh = F2/s2 pipeline.sh + compression retry): 6-cap deep below in the given x-direction (or 6-cup above),
#     exact checks, compression, sat.c face sweep + ext_solve at all 33 positions, brute 32;
#  4. convention B (F2 process26.py): every sweep direction with max cap <= 4, deep-below 6-cap,
#     dedupe, compression; F2 check32.py on every 32-set (exact + compressed): general position,
#     largest convex subset, brute_kgon, sat.c (if |coord| < 2^27), ext_solve 33 positions.
# usage: process_set.sh BIN S.pts OUTROOT KNOWN_FP.jsonl
BIN=$1; F=$2; R=$3; KNOWN=$4; P=/usr/bin/python3
H=$(cd "$(dirname "$0")" && pwd); F2=$H/../../F2
name=$(basename $F .pts); O=$R/$name; mkdir -p $O/scr; cp $F $O/$name.pts
for b in sat ext_solve b33.cnf brute26; do ln -sf $BIN/$b $O/scr/$b; done
$P $F2/scripts/verify26.py $BIN/brute $O/$name.pts > $O/verify26.json 2>&1
$P $H/fingerprint.py $O/fp.jsonl $O/$name.pts > /dev/null
fp=$($P -c "import json;print(json.load(open('$O/fp.jsonl'))['fp'])")
if grep -q "\"fp\": \"$fp\"" $KNOWN; then echo "{\"id\": \"$name\", \"duplicate\": true, \"fp\": \"$fp\"}" > $O/status.json; exit 0; fi
cat $O/fp.jsonl >> $KNOWN
$P -c "
import json,itertools
def o(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
P=sorted(tuple(map(int,l.split())) for l in open('$O/$name.pts') if l.strip())
m=''.join('+' if o(P[i],P[j],P[k])>0 else '-' for i,j,k in itertools.combinations(range(len(P)),3))
print(json.dumps({'id':'$name','points':[list(p) for p in P],'model':m}))" > $O/in.jsonl
bash $H/conva.sh $O/scr $O/convA $O/in.jsonl > $O/convA.log 2>&1
$P $F2/scripts/process26.py $O/convB $O/$name.pts > $O/convB.log 2>&1
ls $O/convB/*.pts > /dev/null 2>&1 && $P $F2/scripts/check32.py $BIN/sat $BIN/ext_solve $BIN/brute_kgon $BIN/b33.cnf $O/wd32 $O/convB/*.pts > $O/convB_check32.jsonl 2>> $O/convB.log
rm -rf $O/scr
echo "{\"id\": \"$name\", \"duplicate\": false, \"fp\": \"$fp\", \"done\": true}" > $O/status.json
