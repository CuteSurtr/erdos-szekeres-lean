#!/bin/bash
# Small-instance runs of close_tree.py: C3T tools (results/C3T/tests/small.py) against C3U tools
# (tests/small.py) without sigma splits, and C3U tools with --sigma-split K.  Output: $W/*.jsonl
# Each run uses its own CaDiCaL work directory (C3U_WORK) and 2 jobs; the conflict limit -c makes
# the timeouts deterministic.
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results
W=${1:-/opt/work/small}; part=${2:-all}
mkdir -p $W
OLD=$R/C3T/tools; NEW=$R/C3U/tools; SO=$R/C3T/tests/small.py; SN=$R/C3U/tests/small.py
for mk in "6 6" "7 6" "8 6"; do set -- $mk
  [ -f $W/base_m$1k$2.cnf ] || python3 $NEW/gen_case.py $1 $2 none -o $W/base_m$1k$2.cnf > /dev/null
done
run() { # TAG TOOLS WRAPPER m k c [extra close_tree options]
  local tag=$1 T=$2 S=$3 m=$4 k=$5 c=$6; shift 6
  rm -rf $W/$tag.jsonl $W/wk_$tag
  local t=$(date +%s)
  C3U_WORK=$W/wk_$tag python3 $S $T $m $k close_tree $W/base_m${m}k${k}.cnf $W/$tag.jsonl 0s0 --jobs 2 --caps 600 --cadopts=-c,$c "$@" > $W/$tag.log 2>&1
  echo "$tag rc=$? records=$(wc -l < $W/$tag.jsonl) $(( $(date +%s) - t ))s $(tail -1 $W/$tag.log)"
  rm -rf $W/wk_$tag
}
if [ $part = all ] || [ $part = cmp ]; then
  # C3T's close_tree has no C3U_WORK: it uses /opt/work/ct, so these runs are sequential
  for x in "6 6 300" "7 6 3000" "7 6 300" "8 6 3000"; do set -- $x
    run cmp_m$1k$2c$3_old $OLD $SO $1 $2 $3
    run cmp_m$1k$2c$3_new $NEW $SN $1 $2 $3
    run cmp_m$1k$2c$3_new0 $NEW $SN $1 $2 $3 --sigma-split 0
  done
fi
if [ $part = all ] || [ $part = sig ]; then
  for x in "6 6 300 2" "7 6 300 2" "7 6 300 3" "7 6 100 2" "8 6 300 2" "8 6 300 3"; do set -- $x
    run sig_m$1k$2c$3K$4 $NEW $SN $1 $2 $3 --sigma-split $4
  done
fi
