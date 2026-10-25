#!/bin/bash
# lane 2 of C3W6 P06: units at positions = 2 (mod 3) of /opt/work/units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921611
LOG=/opt/work/driver2.log
cd $TOOLS
awk -F'\t' 'NR%3==(2+1)%3 {print $2}' /opt/work/units.tsv | while read U; do
  [ -e /opt/work/STOP ] && break
  [ $(date +%s) -lt $END ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct2.cur 2>&1
  cat /opt/work/ct2.cur >> /opt/work/ct2.all
  if grep -q "SAT FOUND" /opt/work/ct2.cur; then grep "SAT FOUND" /opt/work/ct2.cur >> $LOG; touch /opt/work/STOP; fi
  if grep -q "PROOF NOT ACCEPTED" /opt/work/ct2.cur; then grep "PROOF NOT ACCEPTED" /opt/work/ct2.cur >> $LOG; fi
  tail -1 /opt/work/ct2.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
done
echo "=== LANE 2 done $(date -u +%FT%TZ)" >> $LOG
