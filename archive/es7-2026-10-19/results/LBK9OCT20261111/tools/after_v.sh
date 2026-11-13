#!/bin/sh
# after all V solve lanes: cake_lpr checks for cubesV1 and cubesV4, covers, round trips (start only before 04:00)
W=${W:-<lb-k9oct-work-dir>}; cd $W   # set W to the work directory
while systemctl --user is-active -q lb-k9oct-afterg6c; do sleep 15; done
while systemctl --user is-active -q lb-k9oct-vl0 || systemctl --user is-active -q lb-k9oct-vl1 || systemctl --user is-active -q lb-k9oct-vl2 || systemctl --user is-active -q lb-k9oct-vl3 || systemctl --user is-active -q lb-k9oct-g6x2; do sleep 15; done
echo "$(date +%T) V solve lanes finished: V1 $(ls sat/cubesV1/*/solved 2>/dev/null | wc -l)/13, V4 $(ls sat/cubesV4/*/solved 2>/dev/null | wc -l)/13 solved" >> logs/notes.txt
for v in "V1 0" "V4 3"; do set -- $v
  [ "$(date +%H%M)" -ge 0400 ] && [ "$(date +%H%M)" -lt 1200 ] && { echo "$(date +%T) 04:00 reached: no further checks started" >> logs/notes.txt; break; }
  CDIR=$W/sat/cubes$1 NZ=12 ZOFF=$2 HEAP=11000 HEAP2=11000 tools/cubes_g4.sh check 0 1 2 3 4 5 6 7 8 9 10 11 12 > logs/cubecheck_$1.log 2>&1
  python3 tools/verify_cover_mono.py sat/$1/$1.cnf sat/cubes$1 12 $2 > logs/verify_cover_$1.log 2>&1
  tools/roundtrip.sh sat/cubes$1 > logs/roundtrip_$1.log 2>&1
  echo "$(date +%T) $1 checks done: $(grep -l 'VERIFIED_LINES 1' sat/cubes$1/*/result.txt | wc -l) verified; $(tail -n 1 logs/verify_cover_$1.log)" >> logs/notes.txt
done
