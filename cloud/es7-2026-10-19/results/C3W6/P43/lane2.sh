#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921585
K=2
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND" /opt/work/driver*.log; then echo "=== STOP SAT"; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.txt 2>&1
  grep "SAT FOUND\|PROOF NOT ACCEPTED\|unsplittable\": true\|Traceback\|Error" /opt/work/ct$K.txt
  tail -1 /opt/work/ct$K.txt
  echo "=== UNIT $U end $(date -u +%FT%TZ)"
  if grep -q "SAT FOUND" /opt/work/driver*.log /opt/work/ct$K.txt; then echo "=== STOP SAT"; break; fi
done
echo "=== LANE DONE $(date -u +%FT%TZ)"
