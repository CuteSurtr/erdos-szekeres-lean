#!/bin/bash
# close_tree.py findings 2 and 3 (results/C3AUDIT3/REPORT.md), old (results/C3U/tools) against new (results/C3U2/tools).
# m = 5, k = 6 (base gen_case.py 5 6 none in $W), via tests/small.py.  usage: close_tree_tests.sh W
W=$1; R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results; H=$(dirname $(readlink -f $0))
OLD=$R/C3U/tools; NEW=$R/C3U2/tools; B=$W/base_m5k6.cnf; NAT=$R/C3AUDIT3/logs/natural/A_close_tree_0s0_c1.jsonl
ct() { local T=$1 out=$2; shift 2; C3U_WORK=$W/wk_ctt python3 $H/small.py $T 5 6 close_tree $B $out "$@" 2>&1; }
echo "== finding 2: run A of C3AUDIT3 (root 0s0, --caps 600 --cadopts=-c,1, no sigma split) with the new close_tree"
rm -f $W/ctt_A.jsonl; ct $NEW $W/ctt_A.jsonl 0s0 --jobs 2 --caps 600 --cadopts=-c,1 > $W/ctt_A.log
echo "last line: $(tail -1 $W/ctt_A.log | cut -c1-120)..."
python3 - $W/ctt_A.jsonl $W/ctt_A.log $NAT <<'PY'
import json, sys
new = [json.loads(l) for l in open(sys.argv[1])]
last = json.loads(open(sys.argv[2]).read().strip().splitlines()[-1])
old = [json.loads(l) for l in open(sys.argv[3])]
T = {"solve_s", "check_s", "base_sha256"}
key = lambda r: json.dumps({k: v for k, v in r.items() if k not in T}, sort_keys=True)
z_old = sorted(r["node"] for r in old if r.get("split") and r.get("children") == 0)
print("new: split records with 0 children:", sum(1 for r in new if r.get("split") and r.get("children") == 0),
      "| old (C3AUDIT3 run A, C3U 95cafa93):", len(z_old))
print("new open_frontier", last["open_frontier"], "unsplittable", last["unsplittable"],
      "| unsplittable_nodes == the old 0-children split nodes:", sorted(last["unsplittable_nodes"]) == z_old)
a = sorted(key(r) for r in new); b = sorted(key(r) for r in old if not (r.get("split") and r.get("children") == 0))
print("all other records equal to run A (apart from timings and base_sha256):", a == b, len(a), len(b))
PY
echo "== finding 2, restart: the new close_tree on a copy of run A's OUT (old format, 52 split records with 0 children), --hours 0"
cp $NAT $W/ctt_restartA.jsonl
echo "old: $(ct $OLD $W/ctt_restartA.jsonl 0s0 --hours 0 | tail -1)"
echo "new: $(ct $NEW $W/ctt_restartA.jsonl 0s0 --hours 0 | tail -1 | cut -c1-100)..."
echo "== finding 3: OUT holds one certified sigma_cubes.py record {node: 0s0_1, cube: {2: 0}}; ROOT 0s0_1, --hours 0"
for v in OLD NEW; do
  echo '{"node": "0s0_1", "cube": {"2": 0}, "certified": true, "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "status": "UNSATISFIABLE"}' > $W/ctt_cube_$v.jsonl
  echo "$v (root 0s0_1): $(ct ${!v} $W/ctt_cube_$v.jsonl 0s0_1 --hours 0 | tail -1)"
  echo '{"node": "0s0_1", "cube": {"2": 0}, "certified": true, "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "status": "UNSATISFIABLE"}' > $W/ctt_cube_$v.jsonl
  echo "$v (root 0s0_1__2s0): $(ct ${!v} $W/ctt_cube_$v.jsonl 0s0_1__2s0 --hours 0 | tail -1)"
done
