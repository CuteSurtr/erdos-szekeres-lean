#!/bin/sh
# 3d: SAT/UNSAT of c3cnf.py versus symcnf.py (origin/main) on small cases. 
# symcnf: N=3m points, m-fold=3, auxiliary centre, default labelling normal form.
W=${W:-/opt/s/w/cmp}; mkdir -p $W
CAD=/opt/s/cadical/build/cadical
for m in 2 3 4 5 6; do for k in 5 6 7; do
  python3 c3cnf.py $m $k -o $W/c3_${m}_${k}.cnf > /dev/null
  python3 /opt/s/symcnf.py $((3*m)) $k 3 -o $W/sym_${m}_${k}.cnf > $W/sym_${m}_${k}.info
  t0=$(date +%s.%N); a=$(timeout 1800 $CAD -q $W/c3_${m}_${k}.cnf 2>/dev/null | grep '^s' ); t1=$(date +%s.%N)
  b=$(timeout 1800 $CAD -q $W/sym_${m}_${k}.cnf 2>/dev/null | grep '^s'); t2=$(date +%s.%N)
  echo "{\"m\": $m, \"k\": $k, \"c3cnf\": \"${a#s }\", \"c3_s\": $(echo "$t1-$t0" | bc), \"symcnf\": \"${b#s }\", \"sym_s\": $(echo "$t2-$t1" | bc)}"
done; done
