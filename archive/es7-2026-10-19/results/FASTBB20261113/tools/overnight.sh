#!/bin/bash
# overnight.sh C THREADS CONTEXTS [MEM_MB] -- close the residual budget-33 tree for capacity C with fastbb.
#
# Resumable: run the same command again after any interruption.  Closed contexts (ctx-N.json.gz) are kept;
# the master tree (master.txt) is built once and never rebuilt, so the contexts stay the same when rows are
# appended.  A WITNESS (exit code 3) is refuted with cake_lpr-certified coupled rows (witness_kill.py, the
# kill step of capcegar.py), the rows are appended to the extra file, and the search resumes; contexts that
# were closed before stay closed, because rows are only appended and their indices do not move.
#
# Everything is written below $W/overnight.  Nothing in the repository is touched.
set -u
C=$1; THREADS=$2; NCTX=$3; MEM=${4:-6000}
REPO=/home/jay/research/lean/erdos-szekeres-lean
TOOLS=$REPO/cloud/es7-2026-10-19/results/FASTBB20261113/tools
W=/home/jay/research/data/fastbb-20261113
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
SRC=$REPO/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz
D=$W/overnight; mkdir -p $D
EXTRA=$D/capx_c$C.json; ROWS=$D/c$C.rows; OUT=$D/bb_c$C; LOG=$D/c$C.log
KILL=$D/killtools          # private copy of the certification tools (made once, see README)
cd $REPO
# 1. extra rows: the certified coupled rows of capx_c60_i22.json, capacity row h(F) >= 84 - C written first
[ -f $EXTRA ] || $PY $TOOLS/make_capx.py $W/in/capx_c60_i22.json $C $EXTRA $SRC || exit 2
while true; do
  $PY $TOOLS/fastbb_prep.py $SRC $EXTRA $ROWS >> $LOG || exit 2
  $W/build/fastbb solve $ROWS 33 $THREADS $NCTX $OUT --on-witness=continue >> $LOG 2>&1
  rc=$?
  echo "$(date '+%F %T') fastbb exit $rc" >> $LOG
  if [ $rc -eq 0 ]; then
    # exact replay with the unchanged check_tree, one context at a time (memory: one context, not the whole tree)
    $PY $TOOLS/replay_split.py $OUT --jobs $THREADS > $D/c$C.replay.json 2>> $LOG
    echo "$(date '+%F %T') replay: $(cat $D/c$C.replay.json)" >> $LOG
    exit 0
  fi
  if [ $rc -eq 3 ]; then
    if [ ! -d $KILL ]; then echo "WITNESS found; $KILL is missing (see README), stopping" >> $LOG; exit 3; fi
    $PY $TOOLS/witness_kill.py $KILL $EXTRA $OUT >> $LOG 2>&1 || { echo "STUCK: a witness could not be refuted" >> $LOG; exit 1; }
    K=$OUT/witnesses_killed/$(date +%Y%m%d-%H%M%S); mkdir -p $K; mv $OUT/WITNESS.json $OUT/witness-ctx-*.json $K/ 2>/dev/null
    continue
  fi
  exit $rc      # 5 = time limit, 4 = a context exceeded --max-ctx-nodes (use more contexts), 2 = error
done
