#!/bin/bash
# Spot-check lane k: re-solve randomly drawn certified pieces of the 3-fold class from scratch (units6.tsv: phase, node,
# close_tree options, the recorded CNF sha256, the record file). Shared queue via atomic mkdir claims; no new unit within
# 5 minutes of END. close_tree.py unmodified via run_ct.py, cap 3600, both checkers, fresh out files.
k=$1; END=$2; L=$(cd "$(dirname "$0")" && pwd); W=$L/work6
export PATH=$L/bin:$PATH TOOLS=$L/c3u2/cloud/es7-2026-10-19/results/C3U2/tools CT_WORK=$W/ct$k
export CML_HEAP_SIZE=12000 CML_STACK_SIZE=2000
LOG=$W/driver$k.log; i=0
mkdir -p "$CT_WORK" "$W/claims"
while IFS=$'\t' read -r phase node opts sha src; do
  i=$((i + 1))
  [ -e "$W/STOP" ] && { echo "=== STOP flag, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
  [ "$(date +%s)" -lt $((END - 300)) ] || { echo "=== END, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
  mkdir "$W/claims/$i" 2>/dev/null || continue
  echo "=== UNIT $node start $(date -u +%FT%TZ) expect $sha from $src" >> "$LOG"
  res=$(cd "$TOOLS" && python3 "$L/run_ct.py" "$L/work/base.cnf" "$W/out$k.jsonl" "$node" $opts --modeldir "$W/models" 2>&1)
  printf '%s\n' "$res" | tail -2 >> "$LOG"
  echo "=== UNIT $node end $(date -u +%FT%TZ)" >> "$LOG"
  if printf '%s\n' "$res" | grep -q -E "SAT FOUND|PROOF NOT ACCEPTED"; then
    printf '%s\n' "$res" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> "$W/STOP"; exit 1
  fi
done < "$L/units6.tsv"
echo "=== lane $k done $(date -u +%FT%TZ)" >> "$LOG"
