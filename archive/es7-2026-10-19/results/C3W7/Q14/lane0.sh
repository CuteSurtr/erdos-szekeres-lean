#!/bin/bash
# C3W7 Q14 lane 0: units at positions = 0 (mod 3) of units.tsv, cap 900, one solve each
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W7/Q14/units.tsv
END=1792940496
LOG=/opt/work/driver0.log
cd $TOOLS
tail -n +2 $UNITS | cut -f2 | awk 'NR % 3 == (0 + 1) % 3' | while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct0.cur 2>&1
  tail -1 /opt/work/ct0.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct0.cur && { cat /opt/work/ct0.cur >> $LOG; cp /opt/work/ct0.cur /opt/work/alert0.txt; }
done
echo "=== LANE 0 done $(date -u +%FT%TZ)" >> $LOG
