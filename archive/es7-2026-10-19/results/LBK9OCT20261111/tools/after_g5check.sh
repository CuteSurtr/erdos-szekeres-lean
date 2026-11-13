#!/bin/sh
# after the G5 cake_lpr checks: replace G6 lane 0 by 3 lock-aware lanes (cubes started but unsolved are restarted), start the G7 probe
while systemctl --user is-active -q lb-k9oct-g5check; do sleep 15; done
W=${W:-<lb-k9oct-work-dir>}; cd $W   # set W to the work directory
systemctl --user stop lb-k9oct-g6l0
for d in sat/cubes14/c_*; do [ -f $d/solved ] || { rm -f $d/proof.lrat $d/c_*.cnf; rm -rf $d/.lock; }; done
echo "$(date +%T) G6: lane 0 replaced by 3 lock-aware lanes (unsolved cubes restarted)" >> logs/notes.txt
i=0
for order in "0 1 2 3 4 5 6 7 8 9 10" "10 9 8 7 6 5 4 3 2 1 0" "5 6 4 7 3 8 2 9 1 10 0"; do
  systemd-run --user --unit=lb-k9oct-g6x$i -p CPUQuota=100% -p MemoryMax=4000M --working-directory=$W \
    -E BASE=$W/sat/S14/S14.cnf -E CDIR=$W/sat/cubes14 -E NZ=11 -E ZOFF=2 nice -n 10 $W/tools/cubes_g4.sh solve $order
  i=$((i + 1))
done
# G7 probe: monotone on layers 4..12, cube Z_4..Z_12 true (decision list on Z_4..Z_12: ZOFF=3, NZ=9, r = 9)
systemd-run --user --unit=lb-k9oct-g7probe -p CPUQuota=100% -p MemoryMax=4000M --working-directory=$W \
  -E BASE=$W/sat/S15/S15.cnf -E CDIR=$W/sat/cubes15 -E NZ=9 -E ZOFF=3 nice -n 10 $W/tools/cubes_g4.sh solve 9
echo "$(date +%T) G7 probe started: S15 (monotone on layers 4..12), cube Z_4..Z_12 true" >> logs/notes.txt
