#!/bin/bash
# C3W6 P18 lane 1
export PATH=/opt/bin:$PATH
K=1
END=1792921586
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W6/P18/units.tsv
LOG=/opt/work/driver$K.log
tail -n +2 $UNITS | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached $(date -u)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.cur >> $LOG
  tail -1 /opt/work/ct$K.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND" /opt/work/ct$K.cur; then cp /opt/work/ct$K.cur /opt/work/SATFOUND$K.txt; break; fi
done
echo "=== LANE $K done $(date -u '+%F %T')" >> $LOG
