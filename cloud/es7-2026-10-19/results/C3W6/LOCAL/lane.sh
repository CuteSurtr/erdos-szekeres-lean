#!/bin/bash
# Local lane k of NL for the C3W6 shards 4, 5, 8, 22, 37, 41 (units.tsv): exactly the C3W6 per-unit
# command, through run_ct.py (close_tree.py unmodified, work dir redirected). Stops on SAT or rejection.
k=$1; NL=$2; L=$(cd "$(dirname "$0")" && pwd)
export PATH=$L/bin:$PATH TOOLS=$L/c3u2/cloud/es7-2026-10-19/results/C3U2/tools CT_WORK=$L/work/ct$k
export CML_HEAP_SIZE=12000 CML_STACK_SIZE=2000
OUT=$L/work/out$k.jsonl; LOG=$L/work/driver$k.log
i=0
while IFS=$'\t' read -r row node root stratum prior; do
  if [ $((i % NL)) -eq "$k" ]; then
    [ -e "$L/work/STOP" ] && { echo "=== STOP flag, lane $k exits $(date -u +%FT%TZ)" >> "$LOG"; exit 0; }
    echo "=== UNIT $node start $(date -u +%FT%TZ)" >> "$LOG"
    res=$(cd "$TOOLS" && python3 "$L/run_ct.py" "$L/work/base.cnf" "$OUT" "$node" --jobs 1 --sigma-split 3 --sigma-levels 2 \
          --caps 900,600 --cadopts=--sat --hours 0.02 --modeldir "$L/work/models" 2>&1)
    printf '%s\n' "$res" | tail -2 >> "$LOG"
    echo "=== UNIT $node end $(date -u +%FT%TZ)" >> "$LOG"
    if printf '%s\n' "$res" | grep -q -E "SAT FOUND|PROOF NOT ACCEPTED"; then
      printf '%s\n' "$res" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> "$L/work/STOP"; exit 1
    fi
  fi
  i=$((i + 1))
done < "$L/units.tsv"
echo "=== lane $k done $(date -u +%FT%TZ)" >> "$LOG"
