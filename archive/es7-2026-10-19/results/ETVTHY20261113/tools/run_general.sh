#!/bin/bash
# General (a,n) decomposition tests: a-cap-free, n-gon-free sets; Delta (a-1)-cap-free and (n-1)-gon-free (strong).
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
gen() { # capmax gonmax cupmax file
  for s in $(seq 701 730); do for m in box para gauss; do $PY gen_random.py $s $m 8000 $4 $1,$2,$3 > /dev/null; done; done
}
gen 4 5 6 pool_a5n6.jsonl      # a=5 (caps<=4), n=6 (no hexagon)
gen 5 6 7 pool_a6n7.jsonl      # a=6, n=7
gen 3 6 6 pool_a4n7.jsonl      # a=4, n=7
gen 5 7 7 pool_a6n8.jsonl      # a=6, n=8
{
echo "a=5 n=6"; $PY delta_strong_a.py 5 5 pool_a5n6.jsonl
echo "a=6 n=7"; $PY delta_strong_a.py 6 6 pool_a6n7.jsonl
echo "a=4 n=7"; $PY delta_strong_a.py 6 4 pool_a4n7.jsonl
echo "a=6 n=8"; $PY delta_strong_a.py 7 6 pool_a6n8.jsonl
} > general_decomp.log 2>&1
