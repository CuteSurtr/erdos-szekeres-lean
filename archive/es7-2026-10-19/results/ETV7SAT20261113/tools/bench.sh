#!/bin/bash
# usage: bench.sh out.log file1.cnf file2.cnf ...   (sequential, plain cadical, 300 s cap each)
out=$1; shift
for f in "$@"; do
  s=$(date +%s.%N)
  r=$(timeout ${BENCH_T:-300} cadical -q $BENCH_OPTS $f | head -1)
  e=$(date +%s.%N)
  echo "$f $r $(echo "$e - $s" | bc)" >> $out
done
