#!/bin/bash
# Track G2 (phase 2, 13 Nov 2026): close slices 21, 22 (then 20 as an independent second tree) one after the other.
# Usage: run_chain2.sh THREADS   (resumable: run it again; finished slices are skipped, open ones resume)
# Deadline 05:55 KST, 14 Nov (epoch 1794603300).  State and results: runs/s<T>/ (status.json, DONE.json / STUCK.json).
P2=/home/jay/research/data/fastbb-20261113/p2
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
THR=${1:-4}
DL=1794603300
OPTS="--ktop=16 --dtop=8 --klow=4 --sbiter=1000 --max-ctx-nodes=400000"
cd $P2
for spec in "21 4096" "22 4096" "20 4096"; do
  set -- $spec
  T=$1; NCTX=$2
  [ -f runs/s$T/DONE.json ] && continue
  [ -f runs/s$T/STUCK.json ] && continue
  echo "$(date '+%F %T') slice $T: start/resume ($THR threads, $NCTX contexts)" >> runs/chain.log
  $PY -u tools/slicedrv.py $T $THR $NCTX $DL runs/s$T $OPTS >> runs/chain.log 2>&1
  echo "$(date '+%F %T') slice $T: driver exit $?" >> runs/chain.log
  [ $(date +%s) -ge $((DL - 300)) ] && break
done
