#!/bin/bash
export PATH=/opt/bin:$PATH
K=1
END=1792921612
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  [ $(date +%s) -ge $END ] && break
  [ -e /opt/work/STOP ] && { echo "=== STOP"; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/last$K.out 2>&1
  cat /opt/work/last$K.out >> /opt/work/full$K.log
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/last$K.out
  tail -n 1 /opt/work/last$K.out
  echo "=== UNIT $U end $(date -u +%FT%TZ)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/last$K.out; then touch /opt/work/STOP; echo "=== STOP"; break; fi
done
echo "=== LANE DONE $(date -u +%FT%TZ)"
