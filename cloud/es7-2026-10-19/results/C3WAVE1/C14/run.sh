#!/bin/bash
# runner v2: --jobs 3; logs to /opt/work/driver.log (copied into results on commit);
# on PROOF NOT ACCEPTED: kill the driver's pool, re-run the node alone; if accepted, append the record to out.jsonl and resume
export PATH=/opt/bin:$PATH
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C14
END=$(date -u -d "2026-10-20 12:28:00" +%s)
J=${J:-3}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
killall_drv() { pkill -f close_tree.py; sleep 1; pkill -f "cadical -q -t"; pkill -f "cake_lpr /opt/work/ct"; pkill -f "lrat-check /opt/work/ct"; }
for R in $(tail -n +2 $D/roots.tsv | cut -f2); do
 while true; do
  now=$(date +%s); left=$((END-now)); [ $left -le 60 ] && { echo "=== TIME UP"; echo "=== RUNNER DONE $(date -u +%T)"; exit; }
  H=$(python3 -c "print(round($left/3600,3))")
  echo "=== ROOT $R start $(date -u +%T) hours $H jobs $J"
  python3 close_tree.py /opt/work/base.cnf $D/out.jsonl $R --jobs $J --caps 300,300,600 --cadopts=--sat --split-singles --hours $H > /opt/work/cur.log 2>&1 &
  P=$!; ev=""
  while kill -0 $P 2>/dev/null; do
    sleep 5
    grep -q "SAT FOUND\|PROOF NOT ACCEPTED\|Traceback" /opt/work/cur.log && { ev=1; break; }
    [ $(date +%s) -ge $END ] && { ev=time; break; }
  done
  [ -n "$ev" ] && killall_drv
  wait $P; cat /opt/work/cur.log
  echo "=== ROOT $R end $(date -u +%T) ev=$ev"
  if [ "$ev" = time ]; then echo "=== TIME UP (killed)"; echo "=== RUNNER DONE $(date -u +%T)"; exit; fi
  if grep -q "PROOF NOT ACCEPTED" /opt/work/cur.log; then
    N=$(grep "PROOF NOT ACCEPTED" /opt/work/cur.log | awk '{print $4}')
    CAP=$(grep "\"node\": \"$N\"" $D/out.jsonl | tail -1 | python3 -c "import json,sys; print(json.loads(sys.stdin.read())['cap'])")
    echo "=== RECHECK $N alone (cap $CAP)"
    python3 /opt/work/recheck.py $N $CAP > /opt/work/rc.json; cat /opt/work/rc.json >> $D/recheck.jsonl; cat /opt/work/rc.json
    if python3 -c "import json; r=json.load(open('/opt/work/rc.json')); exit(0 if r.get('certified') else 1)"; then
      python3 -c "import json; r=json.load(open('/opt/work/rc.json')); r['base_sha256']='bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da'; print(json.dumps(r))" >> $D/out.jsonl
      echo "=== RECHECK accepted, resuming"; continue
    fi
    echo "=== STOP: real rejection"; echo "=== RUNNER DONE $(date -u +%T)"; exit
  fi
  grep -q "SAT FOUND\|Traceback" /opt/work/cur.log && { echo "=== STOP: needs attention"; echo "=== RUNNER DONE $(date -u +%T)"; exit; }
  break
 done
done
echo "=== RUNNER DONE $(date -u +%T)"
