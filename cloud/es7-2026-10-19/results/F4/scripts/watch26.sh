#!/bin/bash
# Poll the F4 generator outputs; every new realized 26-point set (grow_guided .pts, arm_f /
# realize_models JSONL records with "points") is processed by process_new26.sh, one at a time.
# usage: watch26.sh SCRATCH RUNDIR
S=$1; W=$2; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p $W/new26 $W/proc
while true; do
  /usr/bin/python3 $D/jsonl2pts.py $W/new26 $W/af/*.jsonl > /dev/null 2>&1
  /usr/bin/python3 -c "
import json,os
for l in open('$W/am/realize.jsonl'):
    r=json.loads(l)
    if r.get('realized') and r.get('exact_check') and 'points' in r:
        fn='$W/new26/am%d.pts'%r['model']
        if not os.path.exists(fn): open(fn,'w').write(''.join(f'{x} {y}\n' for x,y in r['points']))" 2>/dev/null
  for f in $W/gg/*.pts; do [ -e "$f" ] && [ ! -e $W/new26/$(basename $f) ] && cp $f $W/new26/; done
  for f in $W/new26/*.pts; do
    [ -e "$f" ] || continue; n=$(basename $f .pts)
    [ -e $W/proc/$n/.done ] && continue
    echo "START $n $(date -u +%H:%M)"
    bash $D/process_new26.sh $S $S/fp_F4.txt $W/proc $f > $W/proc/$n.log 2>&1; rc=$?
    touch $W/proc/$n/.done
    echo "DONE $n rc=$rc $(cat $W/proc/$n/novelty.json 2>/dev/null) $(cat $W/proc/$n/summary.json 2>/dev/null | tr -d '\n ')"
  done
  sleep 30
done
