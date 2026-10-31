#!/bin/bash
# lane L of the cap experiment: its cubes of cubes.tsv in order, each alone as the root of close_tree.py (C3U2 tools at cad4e050)
L=$1; END=$2
export PATH=/opt/bin:$PATH
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/cap/cubes.tsv | awk -v L=$L '$2==L{print $3}' | while read C; do
  NOW=$(date +%s); [ $NOW -ge $END ] && { echo "=== SKIP $C (END)"; continue; }
  echo "=== CUBE $C start $(date -u +%T)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/cap/out_lane$L.jsonl "$C" --caps 1800 --jobs 3 --cadopts=--sat --hours 0.01 2>&1
  echo "=== CUBE $C end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/cap/lane$L.log; then echo "=== STOP"; break; fi
done
echo "=== LANE DONE $(date -u +%T)"
