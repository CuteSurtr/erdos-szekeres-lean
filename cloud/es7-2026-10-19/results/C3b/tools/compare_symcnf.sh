#!/bin/bash
# SAT/UNSAT of gen_c3b.py vs symcnf.py (main) on m = 3..6 orbits, k = 5..7; models saved.
CAD=${CAD:-/tmp/claude-0/build/cadical/build/cadical}
D=${D:-/tmp/claude-0/cmp}; mkdir -p $D
SYM=${SYM:-/tmp/claude-0/symcnf_main.py}
for m in 3 4 5 6; do for k in 5 6 7; do
  n=$((3*m))
  python3 $(dirname $0)/gen_c3b.py $m $k -o $D/b_m${m}k$k.cnf --map $D/b_m${m}k$k.json > /dev/null
  python3 $SYM $n $k 3 -o $D/s_m${m}k$k.cnf --map $D/s_m${m}k$k.json > /dev/null
  t0=$(date +%s.%N); timeout 1800 $CAD -q $D/b_m${m}k$k.cnf > $D/b_m${m}k$k.out; t1=$(date +%s.%N)
  timeout 1800 $CAD -q $D/s_m${m}k$k.cnf > $D/s_m${m}k$k.out; t2=$(date +%s.%N)
  rb=$(head -1 $D/b_m${m}k$k.out | cut -c3-); rs=$(head -1 $D/s_m${m}k$k.out | cut -c3-)
  printf '{"m":%d,"n":%d,"k":%d,"c3b":"%s","c3b_s":%.2f,"symcnf":"%s","symcnf_s":%.2f,"agree":%s}\n' $m $n $k "$rb" $(echo "$t1-$t0"|bc) "$rs" $(echo "$t2-$t1"|bc) $([ "$rb" = "$rs" ] && echo true || echo false)
done; done
