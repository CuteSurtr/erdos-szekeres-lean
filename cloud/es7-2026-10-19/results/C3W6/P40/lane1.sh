#!/bin/bash
# C3W6 P40 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921604
LOG=/opt/work/driver1.log
cd $TOOLS
tail -n +2 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W6/P40/units.tsv | awk -F'\t' 'NR%3==(1+1)%3 {print $2}' > /opt/work/lane1.units
while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached $(date -u)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 < /dev/null > /opt/work/ct1.cur 2>&1
  cat /opt/work/ct1.cur >> /opt/work/ct1.full
  tail -1 /opt/work/ct1.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.cur; then echo "=== STOP flag" >> $LOG; grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.cur >> $LOG; fi
  grep -q "SAT FOUND" /opt/work/ct1.cur && break
done < /opt/work/lane1.units
echo "=== LANE 1 done $(date -u '+%F %T')" >> $LOG
