#!/bin/bash
# One annealing stream: repeated batches of runs until the stop time (epoch seconds).
# usage: run_anneal.sh <mirann> <outdir> <K> <P> <A> <iters> <T0> <T1> <seed0> <stop-epoch>
BIN="$1"; OUT="$2"; K="$3"; P="$4"; A="$5"; IT="$6"; T0="$7"; T1="$8"; SEED="$9"; STOP="${10}"
mkdir -p "$OUT"; cd "$OUT"
PRE="K${K}_P${P}_A${A}_s${SEED}"
while [ "$(date +%s)" -lt "$STOP" ]; do
  "$BIN" anneal "$K" "$P" "$A" "$IT" "$T0" "$T1" "$SEED" 1 "$PRE" | grep -v global_best >> "$PRE.log"
  SEED=$((SEED + 1000))
done
