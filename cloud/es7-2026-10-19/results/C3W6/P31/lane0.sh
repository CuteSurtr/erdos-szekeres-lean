#!/bin/bash
export PATH=/opt/bin:$PATH
K=0
END=1792921594
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
awk -v k=$K '(NR-1)%3==k' /opt/work/units.txt | while read U; do
  [ -e /opt/work/STOP ] && { echo "=== STOP"; break; }
  [ $(date +%s) -ge $END ] && break
  echo "=== UNIT $U start $(date -u +%FT%TZ)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.txt 2>&1
  cat /opt/work/ct$K.txt
  echo "=== UNIT $U end $(date -u +%FT%TZ)"
  echo "=== LAST $(tail -n 1 /opt/work/ct$K.txt)"
  if grep -q "SAT FOUND" /opt/work/ct$K.txt; then touch /opt/work/STOP; echo "=== STOP SAT"; break; fi
  if grep -q "PROOF NOT ACCEPTED" /opt/work/ct$K.txt; then
    echo "=== RECHECK $U start $(date -u +%FT%TZ)"
    python3 close_tree.py /opt/work/base.cnf /opt/work/recheck$K.jsonl $U --jobs 1 --caps 900 --cadopts=--sat --hours 0.02 > /opt/work/rc$K.txt 2>&1
    cat /opt/work/rc$K.txt
    echo "=== RECHECK $U end $(date -u +%FT%TZ)"
    if ! grep -q '"certified": true' /opt/work/rc$K.txt; then touch /opt/work/STOP; echo "=== STOP RECHECK FAILED"; break; fi
  fi
done
echo "=== LANE DONE $(date -u +%FT%TZ)"
