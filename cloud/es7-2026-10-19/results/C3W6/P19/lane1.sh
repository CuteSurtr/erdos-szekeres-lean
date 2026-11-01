#!/bin/bash
# started as: setsid nohup /opt/work/lane.sh 1 > /opt/work/lane1.nohup 2>&1 &
# units: positions == 1 mod 3 of units.tsv (END = start + 4.5 h - 15 min)
# lane runner: $1 = k; END epoch in /opt/work/end_epoch
k=$1
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=$(cat /opt/work/end_epoch)
LOG=/opt/work/driver$k.log
cd $TOOLS
while read -r U; do
  [ -z "$U" ] && continue
  [ $(date -u +%s) -ge $END ] && { echo "=== END reached $(date -u '+%F %T')" >> $LOG; break; }
  [ -e /opt/work/STOP ] && { echo "=== STOP $(date -u '+%F %T')" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$k.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$k.cur 2>&1
  cat /opt/work/ct$k.cur >> /opt/work/ct$k.full
  tail -n 1 /opt/work/ct$k.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct$k.cur; then grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct$k.cur >> $LOG; touch /opt/work/STOP; break; fi
done < /opt/work/units$k.list
echo "=== LANE $k done $(date -u '+%F %T')" >> $LOG
