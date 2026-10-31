#!/bin/bash
# C3W7 Q22 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
K=1
END=1792940494   # 2026-10-25T15:01:34Z = start 10:46:34 + 4.5 h - 15 min
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver$K.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1)%3==k {print $2}' > /opt/work/lane$K.units
while read -r U; do
  [ -e /opt/work/STOP ] && { echo "=== STOP file present, lane stops $(date -u +%FT%TZ)" >> $LOG; break; }
  [ $(( END - $(date +%s) )) -gt 0 ] || { echo "=== END reached $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/ct$K.full
  grep -E 'SAT FOUND|PROOF NOT ACCEPTED' /opt/work/ct$K.cur >> $LOG
  tail -n 1 /opt/work/ct$K.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q 'SAT FOUND' /opt/work/ct$K.cur && touch /opt/work/STOP
done < /opt/work/lane$K.units
echo "=== LANE $K done $(date -u +%FT%TZ)" >> $LOG
