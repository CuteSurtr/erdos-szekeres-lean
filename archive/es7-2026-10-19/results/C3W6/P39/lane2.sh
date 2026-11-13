#!/bin/bash
# C3W6 P39 lane 2: units at positions = 2 (mod 3) of units.tsv (positions from 0, header excluded)
K=2
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=$(cat /opt/work/END)
LOG=/opt/work/driver$K.log
export PATH=/opt/bin:$PATH
tail -n +2 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W6/P39/units.tsv | awk -F'\t' -v k=$K '(NR-1) % 3 == k {print $2}' | while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached before $U $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  (cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02) > /opt/work/ct$K.last 2>&1
  cat /opt/work/ct$K.last >> /opt/work/full$K.log
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.last >> $LOG
  tail -1 /opt/work/ct$K.last >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q "SAT FOUND" /opt/work/ct$K.last && { touch /opt/work/STOP_SAT; break; }
  [ -e /opt/work/STOP_SAT ] && break
done
echo "=== LANE $K done $(date -u +%FT%TZ)" >> $LOG
