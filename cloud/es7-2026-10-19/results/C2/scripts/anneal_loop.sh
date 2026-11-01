#!/bin/bash
# One-core annealing stream for C2: alternates a 33-point run (16 pairs + 1 axis point,
# energy = exact number of convex 7-gons) and a 32-point run (16 pairs, no axis point; every
# heptagon-free set found is axis-scanned exactly by mirann).
# usage: anneal_loop.sh <mirann> <outdir> <iters> <T0> <T1> <seed0> <stop-epoch>
BIN="$1"; OUT="$2"; IT="$3"; T0="$4"; T1="$5"; SEED="$6"; STOP="$7"
mkdir -p "$OUT/m33" "$OUT/m32"
while [ "$(date +%s)" -lt "$STOP" ]; do
  (cd "$OUT/m33" && "$BIN" anneal 7 16 1 "$IT" "$T0" "$T1" "$SEED" 1 "K7_P16_A1_s$SEED" | grep -v global_best >> K7_P16_A1.log)
  [ "$(date +%s)" -lt "$STOP" ] || break
  (cd "$OUT/m32" && "$BIN" anneal 7 16 0 "$IT" "$T0" "$T1" "$((SEED+1))" 1 "K7_P16_A0_s$((SEED+1))" | grep -v global_best >> K7_P16_A0.log)
  SEED=$((SEED + 1000))
done
