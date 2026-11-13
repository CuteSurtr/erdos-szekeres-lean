#!/bin/bash
# Grid of small zcnf.py mirror instances, each evaluated by myeval.py on random exact configurations.
# usage: run_small.sh LOG "t K axis nconf" ...
O=$(cd "$(dirname "$0")" && pwd)
R=${ES7_RESULTS:-$(cd "$O/../.." && pwd)}
log=$1; shift
mkdir -p $O/small; cd $O/small
for spec in "$@"; do
  set -- $spec; t=$1; K=$2; a=$3; n=$4
  f=m_t${t}k${K}a${a}
  [ -f $f.cnf ] || python3 $R/SYMZ/zcnf.py mirror $t $K --axis $a -o $f.cnf --map $f.json > /dev/null
  python3 $O/myeval.py $f.cnf $f.json $t $K $a $n $((1000 * t + 100 * K + a)) >> $log 2>&1
done
echo DONE >> $log
