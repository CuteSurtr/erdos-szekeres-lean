#!/bin/bash
# lane runner: K = lane index; units at positions = K (mod 3) of units.tsv
K=1
END=1792940471   # 15:01:11 UTC = start 10:46:11 + 4.5 h - 15 min
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver$K.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1)%3==k {print $2}' | while read U; do
  now=$(date +%s); [ $((END-now)) -le 0 ] && { echo "=== END reached $(date -u +%T)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/ctfull$K.log
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.cur >> $LOG
  tail -1 /opt/work/ct$K.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  grep -q "^SAT FOUND" /opt/work/ct$K.cur && { echo "=== STOP: SAT FOUND" >> $LOG; break; }
done
echo "=== LANE $K done $(date -u '+%F %T')" >> $LOG
