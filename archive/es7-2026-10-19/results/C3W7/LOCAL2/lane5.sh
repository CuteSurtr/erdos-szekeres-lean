#!/bin/bash
# Local run 5, lane k of 15 (full load for 3 hours) over units5.tsv (phase, node, close_tree options): the 698 C3W7
# nine-bit units still open after run 4, in run 4's order. The lanes share one queue: each takes the next row it can
# claim (an atomic mkdir) and solves it once at cap 3600. No new unit within 5 minutes of END (epoch seconds); the push
# loop kills the lanes at END. close_tree.py unmodified via run_ct.py.
k=$1; END=$2; L=$(cd "$(dirname "$0")" && pwd); W=$L/work5
export PATH=$L/bin:$PATH TOOLS=$L/c3u2/cloud/es7-2026-10-19/results/C3U2/tools CT_WORK=$W/ct$k
export CML_HEAP_SIZE=12000 CML_STACK_SIZE=2000
LOG=$W/driver$k.log; i=0
mkdir -p "$CT_WORK" "$W/claims"
while IFS=$'\t' read -r phase node opts; do
  i=$((i + 1))
  [ -e "$W/STOP" ] && { echo "=== STOP flag, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
  [ "$(date +%s)" -lt $((END - 300)) ] || { echo "=== END, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
  mkdir "$W/claims/$i" 2>/dev/null || continue
  OUT=$W/out$k.jsonl
  echo "=== UNIT $phase $node start $(date -u +%FT%TZ)" >> "$LOG"
  res=$(cd "$TOOLS" && python3 "$L/run_ct.py" "$L/work/base.cnf" "$OUT" "$node" --jobs 1 $opts --modeldir "$W/models" 2>&1)
  printf '%s\n' "$res" | tail -2 >> "$LOG"
  echo "=== UNIT $phase $node end $(date -u +%FT%TZ)" >> "$LOG"
  if printf '%s\n' "$res" | grep -q -E "SAT FOUND|PROOF NOT ACCEPTED"; then
    printf '%s\n' "$res" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> "$W/STOP"; exit 1
  fi
done < "$L/units5.tsv"
echo "=== lane $k done $(date -u +%FT%TZ)" >> "$LOG"
