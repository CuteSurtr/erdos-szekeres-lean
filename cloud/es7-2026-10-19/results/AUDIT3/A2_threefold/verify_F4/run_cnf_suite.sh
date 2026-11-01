#!/bin/bash
# F4 check 2 suite: actual c3cnf.py chain CNF vs exact symmetric sets (one process at a time).
V=$(cd "$(dirname "$0")" && pwd)
cd $V || exit 1
run() { echo "== $*"; /usr/bin/time -p python3 -I cnf_level_check.py "$@" 2>&1; }
SH=disk,ring,cluster,strip
run cnf/c3a_m3k6.cnf cnf/c3a_m3k6.map.json 11 300 $SH
run cnf/c3a_m3k7.cnf cnf/c3a_m3k7.map.json 12 300 $SH
run cnf/c3a_m4k6.cnf cnf/c3a_m4k6.map.json 13 300 $SH
run cnf/c3a_m4k7.cnf cnf/c3a_m4k7.map.json 14 300 $SH
run cnf/c3a_m5k6.cnf cnf/c3a_m5k6.map.json 15 150 $SH
run cnf/c3a_m5k7.cnf cnf/c3a_m5k7.map.json 16 200 cluster,strip,disk
run cnf/c3a_m6k7.cnf cnf/c3a_m6k7.map.json 17 120 cluster,strip
# mutation controls: CNF forbids (k-1)-gons but the truth is "no k-gon" -> must report SOUNDNESS FAIL
run cnf/c3a_m4k6.cnf cnf/c3a_m4k6.map.json 21 60 $SH 7
run cnf/c3a_m5k6.cnf cnf/c3a_m5k6.map.json 22 40 cluster,strip 7
echo DONE
