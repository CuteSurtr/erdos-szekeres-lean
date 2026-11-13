#!/bin/bash
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=$(date -u -d '2026-10-25 11:16:09' +%s)
LOG=/opt/work/driver1.log
cd $TOOLS
for U in 0s0_5_2__1s0-2s1-3s0-4s0-6s0-7s0 0s0_2_3__1s0-3s1-4s0-5s0-6s1-7s0 0s0_1_3__2s0-3s1-4s0-5s0-6s0-7s0; do
  [ $(date +%s) -ge $END ] && break
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --caps 3600 --cadopts=--sat --hours 0.02 > /opt/work/ct_out1_$U.txt 2>&1
  tail -1 /opt/work/ct_out1_$U.txt >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
done
