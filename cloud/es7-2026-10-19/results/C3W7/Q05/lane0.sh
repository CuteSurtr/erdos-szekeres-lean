#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792940495
K=0
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1) % 3 == k' | while read U; do
  [ $(date +%s) -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/full0.log /opt/work/full1.log /opt/work/full2.log 2>/dev/null; then echo "=== STOP $(date -u +%T)" >> /opt/work/driver$K.log; break; fi
  echo "=== UNIT $U start $(date -u +%T)" >> /opt/work/driver$K.log
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/last$K.log 2>&1
  cat /opt/work/last$K.log >> /opt/work/full$K.log
  echo "=== UNIT $U end $(date -u +%T)" >> /opt/work/driver$K.log
  grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/last$K.log >> /opt/work/driver$K.log
  tail -1 /opt/work/last$K.log >> /opt/work/driver$K.log
done
echo "=== LANE DONE $(date -u +%T)" >> /opt/work/driver$K.log
