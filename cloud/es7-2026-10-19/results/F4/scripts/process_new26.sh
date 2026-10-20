#!/bin/bash
# F4 processing of one realized 26-point set (.pts):
#  1. exact checks (F2 verify26.py: general position, x-direction cap/cup, exact lcs, brute.c);
#  2. canonical order-type fingerprint vs. KNOWN (F2, F2/s2 and earlier F4 sets); stop if seen;
#  3. 32-point deep-below sets in both conventions: F2 process26.py (every sweep direction with
#     max cap <= 4, plus compression below 2^27) and F2/s2 build32.py (6-cap below, or 6-cup above
#     after y-reflection, plus compression);
#  4. dedupe the 32-point sets by canonical fingerprint and run F2 check32.py on every file
#     (exact lcs, brute_kgon, sat.c face sweep when |coord| < 2^27, ext_solve at all 33 positions).
# usage: process_new26.sh SCRATCH(bin dir parent) KNOWN_FP OUTROOT set.pts
set -e
S=$1; KNOWN=$2; ROOT=$3; P=$4
D=$(cd "$(dirname "$0")" && pwd); F2=$D/../../F2
PY=/usr/bin/python3
name=$(basename $P .pts); O=$ROOT/$name; mkdir -p $O/f2conv $O/s2conv $O/check
cp $P $O/$name.pts
$PY $F2/scripts/verify26.py $S/bin/brute $O/$name.pts > $O/verify26.json
fp=$($PY $D/fingerprint.py $O/$name.pts | cut -d' ' -f1)
if grep -q "^$fp " $KNOWN; then echo "{\"set\": \"$name\", \"fingerprint\": \"$fp\", \"duplicate_of\": \"$(grep "^$fp " $KNOWN | head -1 | cut -d' ' -f2)\"}" > $O/novelty.json; echo DUP $name; exit 0; fi
echo "$fp $name" >> $KNOWN
echo "{\"set\": \"$name\", \"fingerprint\": \"$fp\", \"duplicate_of\": null}" > $O/novelty.json
$PY $F2/scripts/process26.py $O/f2conv $O/$name.pts > $O/process26.log
$PY -c "
import json; P=[list(map(int,l.split())) for l in open('$O/$name.pts') if l.strip()]
print(json.dumps({'id':'$name','points':P}))" > $O/s2conv/in.jsonl
rm -f $O/s2conv/sets32.jsonl
$PY $F2/s2/scripts/build32.py $O/s2conv/in.jsonl $O/s2conv/sets32.jsonl > $O/s2conv/build32.log
$PY -c "
import json
for l in open('$O/s2conv/sets32.jsonl'):
    r=json.loads(l)
    for k,suf in (('points_exact',''),('points','_small')):
        if k in r:
            open('$O/s2conv/'+r['id']+'_s2'+suf+'.pts','w').write(''.join(f'{x} {y}\n' for x,y in r[k]))"
# retry compression (2 seeds x 150 CPU-s) for direction-scan sets still at |coord| >= 2^27
for f in $O/f2conv/*_d[0-9]*.pts; do case $f in *_small.pts) continue;; esac
  [ -e ${f%.pts}_small.pts ] || $PY $F2/scripts/compress32.py 150 $f >> $O/compress.log; done
ls $O/f2conv/*.pts $O/s2conv/*.pts 2>/dev/null > $O/all32.txt || true
$PY $D/fingerprint.py $(cat $O/all32.txt) > $O/fp32.txt
$PY $F2/scripts/check32.py $S/bin/sat $S/bin/ext_solve $S/bin/brute_kgon $S/b33.cnf $O/check $(cat $O/all32.txt) > $O/check32.jsonl
$PY - $O <<'PY'
import json, sys, os
O = sys.argv[1]; R = [json.loads(l) for l in open(O + "/check32.jsonl")]
fp = {os.path.basename(l.split()[1]): l.split()[0] for l in open(O + "/fp32.txt")}
s = {"files32": len(R), "distinct_order_types32": len(set(fp.values())),
     "all_gp": all(r["general_position"] for r in R), "all_lcs6": all(r["largest_convex_subset"] == 6 for r in R),
     "all_brute_0": all("convex_K_subsets=0" in r["brute_kgon"] for r in R),
     "satc_run": sum(isinstance(r["sat_c"], dict) for r in R),
     "satc_saturated": sum(bool(r.get("geom_saturated")) for r in R),
     "satc_bad": [r["file"] for r in R if isinstance(r["sat_c"], dict) and not r.get("geom_saturated")],
     "ext_saturated": sum(r["abstract_saturated"] for r in R),
     "ext_sat_or_unknown": [r["file"] for r in R if r["ext_sat"] or r["ext_unknown"]]}
d32 = {}
for r in R: d32.setdefault(fp[r["file"]], []).append(r)
s["order_types_with_satc"] = sum(any(isinstance(r["sat_c"], dict) for r in v) for v in d32.values())
s["ALERT"] = bool(s["satc_bad"] or s["ext_sat_or_unknown"] or not (s["all_gp"] and s["all_lcs6"] and s["all_brute_0"]))
json.dump(s, open(O + "/summary.json", "w"), indent=1); print(json.dumps(s))
PY
