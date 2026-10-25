#!/bin/bash
# C3W6 P33 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
K=1
END=1792921606
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/opt/work/units.tsv
LOG=/opt/work/driver$K.log
tail -n +2 $UNITS | cut -f2 | awk -v k=$K '(NR-1) % 3 == k' > /opt/work/lane$K.units
while read -r U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached $(date -u)" >> $LOG; break; }
  grep -q "SAT FOUND" /opt/work/driver*.log 2>/dev/null && { echo "=== stop: SAT FOUND in a lane $(date -u)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.last 2>&1
  cat /opt/work/ct$K.last >> /opt/work/full$K.log
  tail -n 1 /opt/work/ct$K.last >> $LOG
  echo "=== UNIT $U end $(date -u)" >> $LOG
  grep -q "SAT FOUND" /opt/work/ct$K.last && { echo "=== SAT FOUND, lane stops" >> $LOG; grep "SAT FOUND" /opt/work/ct$K.last >> $LOG; break; }
done < /opt/work/lane$K.units
echo "=== LANE $K done $(date -u)" >> $LOG
