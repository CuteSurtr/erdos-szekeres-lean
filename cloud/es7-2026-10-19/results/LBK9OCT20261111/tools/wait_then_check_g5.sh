#!/bin/sh
# wait until the three G5 solve lanes are finished, then run the cake_lpr check lane for cubes13
while systemctl --user is-active -q lb-k9oct-g5l0 || systemctl --user is-active -q lb-k9oct-g5l1 || systemctl --user is-active -q lb-k9oct-g5l2; do sleep 15; done
W=${W:-<lb-k9oct-work-dir>}; cd $W   # set W to the work directory
CDIR=$W/sat/cubes13 NZ=13 ZOFF=1 HEAP=11000 HEAP2=11000 tools/cubes_g4.sh check 0 1 2 3 4 5 6 7 8 9 10 11 12 13 > logs/cubecheck_g5.log 2>&1
python3 tools/verify_cover_mono.py sat/S13/S13.cnf sat/cubes13 13 1 > logs/verify_cover_g5.log 2>&1
tools/roundtrip.sh sat/cubes13 > logs/roundtrip_g5.log 2>&1
