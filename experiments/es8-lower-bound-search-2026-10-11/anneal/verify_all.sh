#!/bin/bash
# Re-verification of the retained point sets; no annealing. Output: $OUT/verify_all.log
# Uses cgon count, brute force (brute.py) and the repository's exact DP
# largest_convex_subset from scripts/es_lower_bound_witness.py.
. "$(dirname "$0")/common.sh"
L="$OUT/verify_all.log"
: > "$L"
{
echo "== repository DP: exactly one convex octagon (common core of all maximum convex subsets)"
python3 verify_core.py out/m65w_raw_s1.txt
python3 verify_core.py out/m65w_mu_s71.txt
echo "== cgon count against brute force: random small sets; witness(5)+1 and witness(6)+1"
python3 brute.py 1 200
python3 brute_addpoint.py
echo "== cgon count: 64-point inputs"
for f in w8.txt v8_1.txt v8_2.txt v8_3.txt; do printf '%s: ' "$f"; "$CGON" count 8 < "$f"; done
echo "== cgon count: 64/65-point outputs and starting sets"
for f in init_w8p_*.txt init_v8p_*.txt out/m65*.txt out/r64*.txt out/r65*.txt; do printf '%s: ' "$f"; "$CGON" count 8 < "$f"; done
echo "== repository DP: 64-point inputs"
for f in w8.txt v8_1.txt v8_2.txt v8_3.txt; do python3 verify.py "$f"; done
echo "== order type: orientation of every index triple of v8_1-v8_3 compared with w8"
python3 - <<'PY'
from itertools import combinations
def sgn(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)
read = lambda f: [tuple(map(int, l.split())) for l in open(f) if l.strip()]
w = read("w8.txt")
for v in (1, 2, 3):
    p = read(f"v8_{v}.txt")
    triples = list(combinations(range(len(w)), 3))
    same = sum(sgn(*(w[i] for i in t)) == sgn(*(p[i] for i in t)) for t in triples)
    print(f"v8_{v}.txt: {same} of {len(triples)} triple orientations equal those of w8.txt")
PY
echo "== repository DP (and brute-force hexagon count for N=16,17): controls"
for f in out/c16_s*.txt out/c17_s*.txt out/c17w_s*.txt; do python3 verify.py "$f" 6; done
for f in out/c32_s*.txt out/c33_s*.txt out/c33w_s*.txt; do python3 verify.py "$f"; done
echo "== DONE"
} >> "$L" 2>&1
cat "$L"
