#!/bin/bash
# Post-process new realized 26-point sets (JSON lines with id, points, model) in both F2 conventions.
# usage: process_new.sh SCRATCH OUTDIR NEW26.jsonl
#  (1) results/F2/s2 convention: pipeline.sh = post26 exact re-check, brute26 (no 5-cap / 7-cup /
#      convex 7-gon), build32 (6-cap deep below in the x-frame, y-reflected if needed), saturate32
#      (sat.c exact face sweep + ext_solve at all 33 positions), brute26 on every 32-set.
#  (2) results/F2 convention: process26.py direction scan (every combinatorially distinct up-direction
#      with max cap <= 4 gets a deep-below 6-cap; realizer-compressed copies *_small.pts), then
#      check32.py on every 32-set (exact gp + lcs, brute_kgon, sat.c if |coord| < 2^27, ext_solve).
set -e
S=$1; O=$2; IN=$3
R=$(cd "$(dirname "$0")/../.." && pwd); PY=/usr/bin/python3
mkdir -p $O/conv_s2 $O/conv_scan/pts26 $O/conv_scan/sets32 $O/conv_scan/wd
bash $R/F2/s2/scripts/pipeline.sh $S $O/conv_s2 $IN
$PY -c "
import json,sys
for l in open('$IN'):
    r=json.loads(l); open('$O/conv_scan/pts26/'+r['id']+'.pts','w').write(''.join(f'{x} {y}\n' for x,y in r['points']))"
$PY $R/F2/scripts/process26.py $O/conv_scan/sets32 $O/conv_scan/pts26/*.pts > $O/conv_scan/process26.log 2>&1
$PY $R/F2/scripts/check32.py $S/sat $S/ext_solve $S/brute_kgon $S/b33.cnf $O/conv_scan/wd $O/conv_scan/sets32/*.pts > $O/conv_scan/check32.jsonl
