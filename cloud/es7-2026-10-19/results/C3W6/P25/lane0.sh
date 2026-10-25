#!/bin/bash
# C3W6 P25 lane 0: units at positions = 0 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
K=0
END=1792921600
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver$K.log
cd $TOOLS
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1)%3==k {print $2}' | while read U; do
  [ -e /opt/work/STOP ] && { echo "=== STOP file present, lane exits $(date -u)" >> $LOG; break; }
  [ $(date +%s) -ge $END ] && { echo "=== END reached, lane exits $(date -u)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/ct$K.full
  echo "last: $(tail -1 /opt/work/ct$K.cur)" >> $LOG
  grep -q "SAT FOUND" /opt/work/ct$K.cur && { echo "SAT FOUND in $U" >> $LOG; touch /opt/work/STOP; }
  grep -q "PROOF NOT ACCEPTED" /opt/work/ct$K.cur && echo "PROOF NOT ACCEPTED in $U" >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
done
echo "=== lane $K done $(date -u '+%F %T')" >> $LOG
