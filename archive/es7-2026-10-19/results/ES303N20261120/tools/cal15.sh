#!/bin/bash
# cal15.sh (20 Nov 2026): cost calibration for a level-15 cube campaign (HEURISTIC timing; any UNSAT leaf is certified
# by p2_cert.sh inside p2_batch_cube.py, exactly as in the level-14 campaign). Runs level-14 depth-0 cubes at L=15,
# easiest first (L14 solve s: hhhhhh 124, hohhhh 244, hhhhho 393), warm-started from the global pilot state
# p2/s15/q.json (676,907 quads). Same options as p2c14_driver_r7.py except --L 15 and the warm file.
# Cube literal order (level-14 split): states 25,12,16,29,17,37; o = 1 = occupied, h = 0 = hole.
# usage: cal15.sh <deadline epoch s>
set -u
W=/home/jay/research/data/n66-20261113; cd $W
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
export ETV_A=4 ETV_B=4 P2_UNIT=esr-n66-cal15
END=$1; mkdir -p p2/cal15
for c in hhhhhh hohhhh hhhhho; do
  left=$(( END - $(date +%s) - 1800 ))            # keep 30 min for p2_cert.sh
  [ $left -lt 1200 ] && { echo "$(date '+%F %T') stop before $c: only $left s left" >> p2/cal15/driver.log; break; }
  lits=""; i=0
  for s in 25 12 16 29 17 37; do b=${c:$i:1}; [ $b = o ] && v=1 || v=0; lits="$lits${lits:+,}$s:$v"; i=$((i+1)); done
  echo "$(date '+%F %T') start $c lits $lits limit $left s" >> p2/cal15/driver.log
  $PY -u p2_batch_cube.py --out p2/cal15/$c.json --dir p2/cal15/$c --L 15 --rows mono/rows_1832.json \
      --warm p2/s15/q.json --seed 11 --tauclose --sb --cube $lits "--cadopts=--unsat -t $left" --secs $left \
      > p2/cal15/$c.out 2>&1
  echo "$(date '+%F %T') end $c rc $? :: $(grep -o '"event": "[^"]*"' p2/cal15/$c.out | paste -sd' ')" >> p2/cal15/driver.log
done
