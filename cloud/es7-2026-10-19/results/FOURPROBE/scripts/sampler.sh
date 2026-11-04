#!/bin/bash
# every 60 s until 09:58: last CaDiCaL report line (seconds, conflicts, irredundant, remaining vars) and proof size
D="<repo>/.cache/es7/final-2026-11-04/four_probe"
while [ $(date +%s) -lt 1793753880 ]; do
  for n in t15 t16 c11111 c11100; do
    f="$D/logs/cad_$n.out"; [ -f "$f" ] || continue
    grep -q '^s \|total real time' "$f" && continue
    l=$(grep -E '^c [*a-zA-Z0-9.!+-]+ +[0-9]' "$f" | tail -1)
    p="$D/$n.lrat"; [ -f "$p" ] || p="$D/cubes17/$n.lrat"
    sz=$(stat -f %z "$p" 2>/dev/null)
    echo "$(date +%H:%M:%S) $n | $l | lrat_bytes=$sz" >> "$D/logs/progress.txt"
  done
  sleep 60
done
