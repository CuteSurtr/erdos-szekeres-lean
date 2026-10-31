#!/bin/bash
# C3W6 P03 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
END=1792921608
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W6/P03/units.tsv
LOG=/opt/work/driver1.log
tail -n +2 $UNITS | cut -f2 | awk 'NR%3==(1+1)%3' | while read U; do
  [ $(( END - $(date +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 < /dev/null > /opt/work/ct1.cur 2>&1
  cat /opt/work/ct1.cur >> /opt/work/ct1.log
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  tail -n 1 /opt/work/ct1.cur >> $LOG
  grep -q "SAT FOUND" /opt/work/ct1.cur && break
done
echo "=== LANE 1 done $(date -u +%FT%TZ)" >> $LOG
