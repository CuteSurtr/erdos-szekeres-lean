#!/bin/bash
# Track G2 (phase 2, 13 Nov 2026), chain v6 = v5 + tools/auto_results.py (data/AUTO_RESULTS.md in the record) after
# every step and every 10 minutes. Close slices 21, 22 one after the other, replay every finished tree a SECOND time
# with the phase-1 wrapper tools/replay_split.py (same trusted check_tree, different wrapper code than verify_slice.py),
# then re-certify every coupled row of the slice-21/22 row files and KEEP the proofs (house rule; recert_keep.py,
# 4 workers), then slice 20 as a second tree with this engine, then slice 23 if time remains.
# Usage: run_chain6.sh THREADS   (resumable: run it again; finished steps are skipped, open ones resume)
# Deadline 05:55 KST, 14 Nov (epoch 1794603300).  State and results: runs/s<T>/ (status.json, DONE.json / STUCK.json,
# replay2.json, replay2_compare.json), proofs/ (recert.jsonl, summary.json, *.zst).
P2=/home/jay/research/data/fastbb-20261113/p2
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
REPO=/home/jay/research/lean/erdos-szekeres-lean
RS=$REPO/cloud/es7-2026-10-19/results/FASTBB20261113/tools/replay_split.py
THR=${1:-5}
DL=1794603300
OPTS="--ktop=16 --dtop=8 --klow=4 --sbiter=1000 --max-ctx-nodes=400000"
cd $P2
AUTO="$PY $P2/tools/auto_results.py"
( while true; do sleep 600; $AUTO > /dev/null 2>&1; done ) &
LOOP=$!
trap 'kill $LOOP 2>/dev/null; $AUTO > /dev/null 2>&1' EXIT
$AUTO > /dev/null 2>&1
slice() {
  T=$1; NCTX=$2
  if [ ! -f runs/s$T/DONE.json ] && [ ! -f runs/s$T/STUCK.json ]; then
    echo "$(date '+%F %T') slice $T: start/resume ($THR threads, $NCTX contexts)" >> runs/chain.log
    $PY -u tools/slicedrv.py $T $THR $NCTX $DL runs/s$T $OPTS >> runs/chain.log 2>&1
    echo "$(date '+%F %T') slice $T: driver exit $?" >> runs/chain.log
    $AUTO > /dev/null 2>&1
  fi
  if [ -f runs/s$T/DONE.json ] && [ ! -f runs/s$T/replay2.json ] && [ $(date +%s) -lt $((DL - 1200)) ]; then
    echo "$(date '+%F %T') slice $T: second replay (replay_split.py --jobs $THR)" >> runs/chain.log
    (cd $REPO && $PY $RS $P2/runs/s$T/bb --jobs $THR > $P2/runs/s$T/replay2.json.tmp 2> $P2/runs/s$T/replay2.err) && mv $P2/runs/s$T/replay2.json.tmp $P2/runs/s$T/replay2.json
    $PY - $P2/runs/s$T >> runs/chain.log 2>&1 <<'EOF'
import json, sys, os
d = sys.argv[1]
a = json.load(open(os.path.join(d, 'DONE.json')))['replay']
lines = [l for l in open(os.path.join(d, 'replay2.json')) if l.strip()]
b = json.loads(lines[-1])
same = (a['nodes'], a['leaves'], a['minimum_margin'], a['pending']) == (b['nodes'], b['leaves'], b['minimum_margin'], b['pending'])
out = {'verify_slice': {k: a[k] for k in ('nodes', 'leaves', 'minimum_margin', 'pending', 'contexts_replayed')},
       'replay_split': {k: b.get(k) for k in ('nodes', 'leaves', 'minimum_margin', 'pending', 'contexts_closed', 'complete_except_state0_branch')},
       'agree': same}
json.dump(out, open(os.path.join(d, 'replay2_compare.json'), 'w'), indent=1)
print(json.dumps(out))
EOF
    echo "$(date '+%F %T') slice $T: second replay done" >> runs/chain.log
    $AUTO > /dev/null 2>&1
  fi
}
mkextra() {
  # row file of a slice not yet started: its two capacity rows + every certified row of the latest slice row file
  T=$1
  [ -f runs/s$T/extra.json ] && return
  mkdir -p runs/s$T
  $PY - $T >> runs/chain.log 2>&1 <<'PYEOF'
import json, os, sys
T = int(sys.argv[1])
src = 'runs/s22/extra.json' if os.path.exists('runs/s22/extra.json') else 'runs/s21/extra.json'
e = json.load(open(src))
assert len(e[0]['support']) == 84 and len(e[1]['support']) == 70 and all(r['rhs'] == 1 for r in e[2:])
rows = [{'support': e[0]['support'], 'rhs': T}, {'support': e[1]['support'], 'rhs': 33 - T}] + e[2:]
json.dump(rows, open(f'runs/s{T}/extra.json', 'w'))
print(json.dumps({'slice': T, 'extra_rows': len(rows), 'from': src}))
PYEOF
}
slice 21 4096
[ $(date +%s) -ge $((DL - 300)) ] && exit 0
slice 22 4096
[ $(date +%s) -ge $((DL - 300)) ] && exit 0
if [ ! -f proofs/summary.json ] || [ -n "$(find runs/s22/extra.json -newer proofs/summary.json 2>/dev/null)" ]; then
  echo "$(date '+%F %T') re-certification with kept proofs (recert_keep.py, 4 workers)" >> runs/chain.log
  EX="runs/s21/extra.json"; [ -f runs/s22/extra.json ] && EX="$EX runs/s22/extra.json"
  $PY -u tools/recert_keep.py proofs 4 $EX >> runs/chain.log 2>&1
  echo "$(date '+%F %T') re-certification exit $?" >> runs/chain.log
  $AUTO > /dev/null 2>&1
fi
[ $(date +%s) -ge $((DL - 300)) ] && exit 0
mkextra 20
slice 20 4096
[ $(date +%s) -ge $((DL - 300)) ] && exit 0
mkextra 23
slice 23 4096
echo "$(date '+%F %T') chain6 finished" >> runs/chain.log
