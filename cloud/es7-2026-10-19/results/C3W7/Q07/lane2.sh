#!/bin/bash
# C3W7 Q07 lane 2: units at positions = 2 (mod 3) of units.tsv
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940494
export PATH=/opt/bin:$PATH
cd $TOOLS
awk 'NR%3==(2+1)%3' /opt/work/units.txt | while read U; do
  [ $(date -u +%s) -lt $END ] || break
  grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log && { echo "=== STOP flag seen $(date -u)" >> /opt/work/driver2.log; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> /opt/work/driver2.log
  python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct2.cur 2>&1
  cat /opt/work/ct2.cur >> /opt/work/lane2.full
  grep -h "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct2.cur >> /opt/work/driver2.log
  tail -1 /opt/work/ct2.cur >> /opt/work/driver2.log
  echo "=== UNIT $U end $(date -u '+%F %T')" >> /opt/work/driver2.log
done
echo "=== LANE 2 done $(date -u '+%F %T')" >> /opt/work/driver2.log
