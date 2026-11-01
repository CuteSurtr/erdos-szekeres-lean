#!/bin/bash
# Local lane k of NL over units2.tsv (phase, node, close_tree options): phase A = C3W6 timeouts re-solved at cap 3600,
# phase B = H3/one six-bit cubes split once more on sigma (nine-bit cubes at cap 900). close_tree.py unmodified via run_ct.py.
k=$1; NL=$2; L=$(cd "$(dirname "$0")" && pwd)
export PATH=$L/bin:$PATH TOOLS=$L/c3u2/cloud/es7-2026-10-19/results/C3U2/tools CT_WORK=$L/work2/ct$k
export CML_HEAP_SIZE=12000 CML_STACK_SIZE=2000
LOG=$L/work2/driver$k.log; i=0
while IFS=$'\t' read -r phase node opts; do
  if [ $((i % NL)) -eq "$k" ]; then
    [ -e "$L/work2/STOP" ] && { echo "=== STOP flag, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
    OUT=$L/work2/out$phase$k.jsonl
    echo "=== UNIT $phase $node start $(date -u +%FT%TZ)" >> "$LOG"
    res=$(cd "$TOOLS" && python3 "$L/run_ct.py" "$L/work/base.cnf" "$OUT" "$node" --jobs 1 $opts --modeldir "$L/work2/models" 2>&1)
    printf '%s\n' "$res" | tail -2 >> "$LOG"
    echo "=== UNIT $phase $node end $(date -u +%FT%TZ)" >> "$LOG"
    if printf '%s\n' "$res" | grep -q -E "SAT FOUND|PROOF NOT ACCEPTED"; then
      printf '%s\n' "$res" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> "$L/work2/STOP"; exit 1
    fi
  fi
  i=$((i + 1))
done < "$L/units2.tsv"
echo "=== lane $k done $(date -u +%FT%TZ)" >> "$LOG"
