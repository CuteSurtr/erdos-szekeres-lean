#!/bin/bash
# C3W6 P14 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921573
LOG=/opt/work/driver1.log
mkdir -p /opt/work/ct /opt/work/models
cd $TOOLS
awk -F'\t' 'NR>1 && ((NR-2) % 3 == 1) {print $2}' /opt/work/units.tsv | while read U; do
  [ $(( END - $(date +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 < /dev/null > /opt/work/ct_1.last 2>&1
  cat /opt/work/ct_1.last >> /opt/work/driver1.full
  echo "$(tail -1 /opt/work/ct_1.last)" >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct_1.last; then grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct_1.last >> $LOG; fi
  grep -q "SAT FOUND" /opt/work/ct_1.last && break
done
echo "=== LANE 1 done $(date -u +%FT%TZ)" >> $LOG
