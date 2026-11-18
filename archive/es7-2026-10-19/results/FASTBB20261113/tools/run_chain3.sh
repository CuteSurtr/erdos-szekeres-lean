#!/bin/bash
# Track G2 (phase 2, 13 Nov 2026): close slices 21, 22 (then 20 as an independent second tree) one after the other,
# and replay every finished tree a SECOND time with the phase-1 wrapper tools/replay_split.py (same trusted
# check_tree, different wrapper code than verify_slice.py), right after it is closed.
# Usage: run_chain3.sh THREADS   (resumable: run it again; finished slices are skipped, open ones resume)
# Deadline 05:55 KST, 14 Nov (epoch 1794603300).  State and results: runs/s<T>/ (status.json, DONE.json / STUCK.json,
# replay2.json, replay2_compare.json).
P2=/home/jay/research/data/fastbb-20261113/p2
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
REPO=/home/jay/research/lean/erdos-szekeres-lean
RS=$REPO/cloud/es7-2026-10-19/results/FASTBB20261113/tools/replay_split.py
THR=${1:-5}
DL=1794603300
OPTS="--ktop=16 --dtop=8 --klow=4 --sbiter=1000 --max-ctx-nodes=400000"
cd $P2
for spec in "21 4096" "22 4096" "20 4096"; do
  set -- $spec
  T=$1; NCTX=$2
  if [ ! -f runs/s$T/DONE.json ] && [ ! -f runs/s$T/STUCK.json ]; then
    echo "$(date '+%F %T') slice $T: start/resume ($THR threads, $NCTX contexts)" >> runs/chain.log
    $PY -u tools/slicedrv.py $T $THR $NCTX $DL runs/s$T $OPTS >> runs/chain.log 2>&1
    echo "$(date '+%F %T') slice $T: driver exit $?" >> runs/chain.log
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
  fi
  [ $(date +%s) -ge $((DL - 300)) ] && break
done
echo "$(date '+%F %T') chain3 finished" >> runs/chain.log
