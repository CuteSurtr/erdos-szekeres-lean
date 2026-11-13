#!/bin/sh
# after the G6 solve lanes: cake_lpr checks of cubes14, cover, round trips; then 3 lock-aware G7 lanes
W=${W:-<lb-k9oct-work-dir>}; cd $W   # set W to the work directory
while systemctl --user is-active -q lb-k9oct-g6x0 || systemctl --user is-active -q lb-k9oct-g6x1 || systemctl --user is-active -q lb-k9oct-g6x2; do sleep 15; done
echo "$(date +%T) G6 solve lanes finished ($(ls sat/cubes14/*/solved | wc -l) cubes solved); starting G6 cake_lpr checks" >> logs/notes.txt
CDIR=$W/sat/cubes14 NZ=11 ZOFF=2 HEAP=11000 HEAP2=11000 tools/cubes_g4.sh check 0 1 2 3 4 5 6 7 8 9 10 11 > logs/cubecheck_g6.log 2>&1
python3 tools/verify_cover_mono.py sat/S14/S14.cnf sat/cubes14 11 2 > logs/verify_cover_g6.log 2>&1
tools/roundtrip.sh sat/cubes14 > logs/roundtrip_g6.log 2>&1
echo "$(date +%T) G6 checks done: $(grep -l 'VERIFIED_LINES 1' sat/cubes14/*/result.txt | wc -l) verified; $(tail -n 1 logs/verify_cover_g6.log)" >> logs/notes.txt
if [ "$(date +%H%M)" -lt 0330 ] || [ "$(date +%H%M)" -gt 2000 ]; then
  i=0
  for order in "0 1 2 3 4 5 6 7 8" "8 7 6 5 4 3 2 1 0" "4 5 3 6 2 7 1 8 0"; do
    systemd-run --user --unit=lb-k9oct-g7x$i -p CPUQuota=100% -p MemoryMax=4000M --working-directory=$W \
      -E BASE=$W/sat/S15/S15.cnf -E CDIR=$W/sat/cubes15 -E NZ=9 -E ZOFF=3 nice -n 10 $W/tools/cubes_g4.sh solve $order
    i=$((i + 1))
  done
  echo "$(date +%T) started 3 G7 lanes (cubes c_0..c_8 of S15)" >> logs/notes.txt
fi
