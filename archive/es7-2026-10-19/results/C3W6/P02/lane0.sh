#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921602
K=0
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
awk -v k=$K '(NR-1)%3==k' /opt/work/units.txt | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND" /opt/work/full0.log /opt/work/full1.log /opt/work/full2.log 2>/dev/null; then echo "=== STOP SAT"; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)"
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> /opt/work/full$K.log
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/unit$K.out 2>&1
  cat /opt/work/unit$K.out >> /opt/work/full$K.log
  tail -n 1 /opt/work/unit$K.out
  echo "=== UNIT $U end $(date -u +%FT%TZ)"
  if grep -q "SAT FOUND" /opt/work/unit$K.out; then echo "=== STOP SAT"; break; fi
done
echo "=== LANE DONE $(date -u +%FT%TZ)"
