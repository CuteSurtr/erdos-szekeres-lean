#!/bin/bash
# lane runner: lane K takes units at positions = K (mod 3) of units.tsv (counted from 0)
K=$1
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=$(cat /opt/work/END)
LOG=/opt/work/driver$K.log
cd $TOOLS
i=0
while read U; do
  if [ $((i % 3)) -eq $K ]; then
    [ -e /opt/work/STOP ] && { echo "=== STOP flag, lane $K exits $(date -u +%FT%TZ)" >> $LOG; exit 0; }
    [ $(date +%s) -ge $END ] && { echo "=== END reached, lane $K exits $(date -u +%FT%TZ)" >> $LOG; exit 0; }
    echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
    python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.tmp 2>&1
    cat /opt/work/ct$K.tmp >> $LOG
    echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
    if grep -q "SAT FOUND" /opt/work/ct$K.tmp; then touch /opt/work/STOP; echo "=== SAT FOUND, all lanes stop" >> $LOG; exit 0; fi
    if grep -q "PROOF NOT ACCEPTED" /opt/work/ct$K.tmp; then
      echo "=== RECHECK $U start $(date -u +%FT%TZ)" >> $LOG
      python3 close_tree.py /opt/work/base.cnf /opt/work/recheck.jsonl $U --jobs 1 --caps 900 --cadopts=--sat --hours 0.02 >> $LOG 2>&1
      ok=$(python3 -c "import json,sys;r=[json.loads(l) for l in open('/opt/work/recheck.jsonl') if l.strip()];r=[x for x in r if x.get('node')=='$U' and 'status' in x];print(1 if r and r[-1].get('certified') and r[-1].get('lrat_check')=='c VERIFIED' and r[-1].get('cake_lpr')=='s VERIFIED UNSAT' else 0)")
      echo "=== RECHECK $U end $(date -u +%FT%TZ) accepted=$ok" >> $LOG
      [ "$ok" = 1 ] || { touch /opt/work/STOP; echo "=== RECHECK REJECTED, all lanes stop" >> $LOG; exit 0; }
    fi
  fi
  i=$((i+1))
done < /opt/work/units.list
echo "=== lane $K done $(date -u +%FT%TZ)" >> $LOG
