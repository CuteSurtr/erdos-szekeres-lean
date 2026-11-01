#!/bin/bash
# Full processing of one realized 26-point set S (pts file, one "x y" per line).
# usage: process_set.sh NAME S.pts OUTDIR
# needs in $W: brute (F2/scripts/brute.c), brute26 (F2/s2/scripts/brute26.c), brute_kgon
# (tools/trackB/brute_kgon.c), sat (tools/trackA/sat.c), ext_solve (results/A/scripts/ext_solve.cpp),
# b33.cnf (tools/trackB/gen_cnf.py 33 7).
# 1. exact 26-point checks: verify26.py (Python DP + brute.c) and brute26 26 5 7 7 (no 5-cap, 7-cup, 7-gon)
# 2. canonical order-type fingerprint (dedup against F2 and earlier F5 sets is done by the caller)
# 3. 32-point deep-below sets, both F2 conventions:
#    (a) F2 process26.py: every sweep direction with max cap <= 4, 6-cap deep below (+ compressed copy)
#    (b) F2/s2 build32.py: x-direction, 6-cap deep below (or 6-cup above after y-reflection)
# 4. every 32-point set: F2 check32.py (general position, exact lcs, brute_kgon, sat.c over all faces
#    when |coord| < 2^27, ext_solve one-point extension at all 33 x-positions)
set -e
W=${W:-/tmp/claude-0/w}; NAME=$1; SP=$2; O=$3
F2=$(cd "$(dirname "$0")/../../F2" && pwd)
mkdir -p $O/sets32 $O/work
cp $SP $O/$NAME.pts
/usr/bin/python3 $F2/scripts/verify26.py $W/brute $O/$NAME.pts > $O/verify26.json
/usr/bin/python3 -c "
import itertools,sys
P=sorted(tuple(map(int,l.split())) for l in open('$O/$NAME.pts') if l.strip())
o=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
print(''.join('+' if o(P[i],P[j],P[k])>0 else '-' for i,j,k in itertools.combinations(range(len(P)),3)))" | $W/brute26 26 5 7 7 > $O/brute26.txt
/usr/bin/python3 $(dirname "$0")/fingerprint.py $O/$NAME.pts > $O/fingerprint.txt
/usr/bin/python3 $F2/scripts/process26.py $O/sets32 $O/$NAME.pts > $O/process26.log
python3 -c "
import json
P=[list(map(int,l.split())) for l in open('$O/$NAME.pts') if l.strip()]
print(json.dumps({'id':'$NAME','points':P}))" > $O/S.jsonl
rm -f $O/work/build32.jsonl
/usr/bin/python3 $F2/s2/scripts/build32.py $O/S.jsonl $O/work/build32.jsonl > $O/build32_s2.log
/usr/bin/python3 -c "
import json
for l in open('$O/work/build32.jsonl'):
    r=json.loads(l)
    if 'points_exact' not in r: continue
    open('$O/sets32/${NAME}_x.pts','w').write(''.join(f'{x} {y}\n' for x,y in r['points_exact']))
    if r.get('compressed_ok') and r['compressed_max']<2**27 and r['points']!=r['points_exact']:
        open('$O/sets32/${NAME}_x_small.pts','w').write(''.join(f'{x} {y}\n' for x,y in r['points']))"
/usr/bin/python3 $F2/scripts/check32.py $W/sat $W/ext_solve $W/brute_kgon $W/b33.cnf $O/work $O/sets32/*.pts > $O/check32.jsonl
/usr/bin/python3 - $O <<'PY'
import json, sys, glob
O = sys.argv[1]
R = [json.loads(l) for l in open(O + "/check32.jsonl")]
v = json.load(open(O + "/verify26.json"))
s = {"n32": len(R),
     "all_gp": all(r["general_position"] for r in R), "max_lcs": max((r["largest_convex_subset"] for r in R), default=None),
     "brute_kgon": sorted({r["brute_kgon"].split("\n")[-1][:80] for r in R}),
     "sat_c_run": sum(isinstance(r["sat_c"], dict) for r in R),
     "geom_saturated": sum(bool(r.get("geom_saturated")) for r in R),
     "geom_bad": [r["file"] for r in R if isinstance(r["sat_c"], dict) and (r["sat_c"].get("bad_candidates") or not r.get("faces_covered"))],
     "abstract_saturated": sum(r["abstract_saturated"] for r in R),
     "ext_sat": {r["file"]: r["ext_sat"] for r in R if r["ext_sat"]},
     "ext_unknown": {r["file"]: r["ext_unknown"] for r in R if r["ext_unknown"]},
     "verify26": v, "brute26": open(O + "/brute26.txt").read().strip(),
     "fingerprint": open(O + "/fingerprint.txt").read().split()[1]}
json.dump(s, open(O + "/summary.json", "w"), indent=1); print(json.dumps(s))
PY
