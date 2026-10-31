#!/bin/bash
# C3W6 P09 lane 0: units at positions = 0 (mod 3) of units.tsv, one close_tree.py run per unit at cap 900
export PATH=/opt/bin:$PATH
K=0
END=1792921612
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver$K.log
cd $TOOLS
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1) % 3 == k {print $2}' | while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached before $U $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.out 2>&1
  rc=$?
  echo "=== UNIT $U end $(date -u +%FT%TZ) rc=$rc" >> $LOG
  tail -n 1 /opt/work/ct$K.out >> $LOG
  cat /opt/work/ct$K.out >> /opt/work/ct$K.all
  if grep -q -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.out; then echo "=== FLAG $U" >> $LOG; grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.out >> $LOG; grep -q "SAT FOUND" /opt/work/ct$K.out && break; fi
done
echo "=== LANE $K done $(date -u +%FT%TZ)" >> $LOG
