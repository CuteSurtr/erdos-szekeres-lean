#!/bin/sh
# V1 checks as soon as at most one V solve lane is active; V4 checks when all V lanes are finished (start before 04:00)
W=${W:-<lb-k9oct-work-dir>}; cd $W   # set W to the work directory
nact() { n=0; for u in vl0 vl1 vl2 vl3; do systemctl --user is-active -q lb-k9oct-$u && n=$((n + 1)); done; echo $n; }
while [ $(nact) -gt 1 ]; do sleep 15; done
echo "$(date +%T) at most one V lane active: starting V1 cake_lpr checks" >> logs/notes.txt
CDIR=$W/sat/cubesV1 NZ=12 ZOFF=0 HEAP=11000 HEAP2=11000 tools/cubes_g4.sh check 0 1 2 3 4 5 6 7 8 9 10 11 12 > logs/cubecheck_V1.log 2>&1
python3 tools/verify_cover_mono.py sat/V1/V1.cnf sat/cubesV1 12 0 > logs/verify_cover_V1.log 2>&1
tools/roundtrip.sh sat/cubesV1 > logs/roundtrip_V1.log 2>&1
echo "$(date +%T) V1 checks done: $(grep -l 'VERIFIED_LINES 1' sat/cubesV1/*/result.txt | wc -l) verified; $(tail -n 1 logs/verify_cover_V1.log)" >> logs/notes.txt
while [ $(nact) -gt 0 ]; do sleep 15; done
echo "$(date +%T) V lanes finished: V4 $(ls sat/cubesV4/*/solved 2>/dev/null | wc -l)/13 solved" >> logs/notes.txt
if [ "$(date +%H%M)" -ge 0400 ]; then echo "$(date +%T) 04:00 reached: V4 checks not started" >> logs/notes.txt; exit 0; fi
CDIR=$W/sat/cubesV4 NZ=12 ZOFF=3 HEAP=11000 HEAP2=11000 tools/cubes_g4.sh check 0 1 2 3 4 5 6 7 8 9 10 11 12 > logs/cubecheck_V4.log 2>&1
python3 tools/verify_cover_mono.py sat/V4/V4.cnf sat/cubesV4 12 3 > logs/verify_cover_V4.log 2>&1
tools/roundtrip.sh sat/cubesV4 > logs/roundtrip_V4.log 2>&1
echo "$(date +%T) V4 checks done: $(grep -l 'VERIFIED_LINES 1' sat/cubesV4/*/result.txt | wc -l) verified; $(tail -n 1 logs/verify_cover_V4.log)" >> logs/notes.txt
