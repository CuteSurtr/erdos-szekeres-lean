#!/bin/bash
# summarize.sh : per run, the answer line, conflicts (total and per second), decisions, process time, peak RSS
D="<repo>/.cache/es7/final-2026-11-04/four_probe"
for n in t15 t16 c11111 c11100; do
  f="$D/logs/cad_$n.out"; [ -f "$f" ] || continue
  echo "== $n: $(grep -m1 '^s ' "$f" || echo 's (none: time limit)')"
  grep -E '^c (conflicts|decisions|propagations|fixed|learned|restarts):' "$f"
  grep -E 'total process time|total real time|maximum resident' "$f"
done
