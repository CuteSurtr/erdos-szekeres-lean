#!/bin/bash
# C3W6 P36 lane 2: units at positions = 2 (mod 3) of units.tsv, one close_tree run per unit at cap 900
K=2; END=1792921608
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver$K.log; OUT=/opt/work/out$K.jsonl
export PATH=/opt/bin:$PATH
# watchdog: close_tree checks its deadline only between batches, so kill this lane's process group at END
( sleep $((END - $(date +%s))); echo "=== END watchdog kill $(date -u '+%F %T')" >> $LOG; kill -TERM -$$ ) &
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1) % 3 == k {print $2}' | while read U; do
  [ $((END - $(date +%s))) -gt 0 ] || break
  [ -e /opt/work/STOP ] && break
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf $OUT $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/ct$K.full
  echo "$(tail -1 /opt/work/ct$K.cur)" >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND" /opt/work/ct$K.cur; then
    grep "SAT FOUND" /opt/work/ct$K.cur >> $LOG; touch /opt/work/STOP; echo SAT > /opt/work/STOP; break
  fi
  if grep -q "PROOF NOT ACCEPTED" /opt/work/ct$K.cur; then
    grep "PROOF NOT ACCEPTED" /opt/work/ct$K.cur >> $LOG
    echo "=== RECHECK $U start $(date -u '+%F %T')" >> $LOG
    python3 close_tree.py /opt/work/base.cnf /opt/work/recheck.jsonl $U --jobs 1 --caps 900 --cadopts=--sat --hours 0.02 > /opt/work/rc$K.cur 2>&1
    cat /opt/work/rc$K.cur >> $LOG
    if ! grep -q '"certified": true' /opt/work/rc$K.cur; then echo "PROOF REJECTED $U" > /opt/work/STOP; break; fi
  fi
done
echo "=== LANE $K done $(date -u '+%F %T')" >> $LOG
kill %1 2>/dev/null
