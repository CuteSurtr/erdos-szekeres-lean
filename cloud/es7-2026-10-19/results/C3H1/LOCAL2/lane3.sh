#!/bin/bash
# Local lane k of NL over units3.tsv (phase C, node, close_tree options): the nine-bit sigma-cubes of the 80 H3/one
# six-bit cubes not in C3W7, each solved once at cap 3600. close_tree.py unmodified via run_ct.py.
k=$1; NL=$2; L=$(cd "$(dirname "$0")" && pwd)
export PATH=$L/bin:$PATH TOOLS=$L/c3u2/cloud/es7-2026-10-19/results/C3U2/tools CT_WORK=$L/work3/ct$k
export CML_HEAP_SIZE=12000 CML_STACK_SIZE=2000
LOG=$L/work3/driver$k.log; i=0
while IFS=$'\t' read -r phase node opts; do
  if [ $((i % NL)) -eq "$k" ]; then
    [ -e "$L/work3/STOP" ] && { echo "=== STOP flag, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
    OUT=$L/work3/out$phase$k.jsonl
    echo "=== UNIT $phase $node start $(date -u +%FT%TZ)" >> "$LOG"
    res=$(cd "$TOOLS" && python3 "$L/run_ct.py" "$L/work/base.cnf" "$OUT" "$node" --jobs 1 $opts --modeldir "$L/work3/models" 2>&1)
    printf '%s\n' "$res" | tail -2 >> "$LOG"
    echo "=== UNIT $phase $node end $(date -u +%FT%TZ)" >> "$LOG"
    if printf '%s\n' "$res" | grep -q -E "SAT FOUND|PROOF NOT ACCEPTED"; then
      printf '%s\n' "$res" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> "$L/work3/STOP"; exit 1
    fi
  fi
  i=$((i + 1))
done < "$L/units3.tsv"
echo "=== lane $k done $(date -u +%FT%TZ)" >> "$LOG"
