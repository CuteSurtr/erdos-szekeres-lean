#!/bin/bash
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940476
k=1
LOG=/opt/work/driver$k.log
i=0
while read U; do
  if [ $((i % 3)) -eq $k ]; then
    if [ $(( END - $(date +%s) )) -le 0 ]; then echo "=== END reached before $U $(date -u +%FT%TZ)" >> $LOG; break; fi
    echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
    cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$k.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$k.last 2>&1
    cat /opt/work/ct$k.last >> /opt/work/ct$k.full
    echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
    tail -1 /opt/work/ct$k.last >> $LOG
    if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct$k.last; then echo "=== STOP lane $k" >> $LOG; break; fi
  fi
  i=$((i+1))
done < /opt/work/units.list
echo "=== LANE $k done $(date -u +%FT%TZ)" >> $LOG
