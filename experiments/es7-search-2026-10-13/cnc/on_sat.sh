#!/bin/sh
# Waits (locally, no LLM) for the ES(7) cube-and-conquer run to stop. On a SAT model it decodes the
# triple orientations, re-checks the signotope axiom and the absence of convex 7-gons by brute force,
# and writes RESULT.txt. A SAT model is ABSTRACT: realizability must still be established.
cd "$(dirname "$0")"
RUN=${1:-run33}; N=${2:-33}; K=${3:-7}
while kill -0 "$(cat $RUN.pid)" 2>/dev/null; do sleep 60; done
python3 - "$RUN" "$N" > "$RUN/RESULT.txt" <<'PY'
import json, sys, itertools
run, n = sys.argv[1], int(sys.argv[2])
st = json.load(open(f'{run}/state.json'))
if not st.get('sat'):
    print('no SAT model; open cubes:', len(st['open']), 'closed weight:', st['closed_weight']); sys.exit()
vals = {abs(int(l)): int(l) > 0 for l in open(f"{run}/{st['sat']['model']}")}
with open(f'{run}/model.sig', 'w') as f:
    for v, (i, j, k) in enumerate(itertools.combinations(range(1, n + 1), 3), 1):
        f.write(f"{i} {j} {k} {1 if vals[v] else -1}\n")
print('SAT model decoded to', f'{run}/model.sig', '(abstract signotope; brute-force check follows)')
PY
[ -f "$RUN/model.sig" ] && ../trackB-sat/brute_kgon "$N" "$K" "$RUN/model.sig" >> "$RUN/RESULT.txt" 2>&1
date >> "$RUN/RESULT.txt"
