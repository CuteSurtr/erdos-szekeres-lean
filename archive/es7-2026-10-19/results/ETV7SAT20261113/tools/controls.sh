#!/bin/bash
# positive controls on real point sets (README section 5)
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
set -x
mkdir -p ctl
# 1. lemma rows on the 26-point ETV set
$PY addrows.py om/t57_N26.cnf ctl/t57_N26_v1.cnf S1:25 S2:25 B1:16 B2:16 > ctl/addrows26.log 2>&1
$PY owner_check.py pts/etv757.json ctl/t57_N26_v1.cnf > ctl/check_v1_26.log 2>&1
$PY owner_check.py pts/etv757.json ctl/t57_N26_v1.cnf --mirror >> ctl/check_v1_26.log 2>&1
# 2. random sets: hexagon model (3,4,6), (5,6)-heptagon model (3,4,7), target model (3,5,7), all with N=2
$PY owner.py 3 4 6 2 ctl/hx_N2.cnf --names > ctl/gen_hx.log 2>&1
$PY owner.py 3 4 7 2 ctl/s56_N2.cnf --names > ctl/gen_s56.log 2>&1
$PY owner.py 3 5 7 2 ctl/t57_N2.cnf --names > ctl/gen_t57.log 2>&1
$PY addrows.py ctl/t57_N2.cnf ctl/t57_N2_v1.cnf S1:25 S2:25 B1:16 B2:16 > ctl/addrows2.log 2>&1
$PY randsets.py 4 5 6 24 101 pts/rhx > ctl/rand_hx.log 2>&1
$PY randsets.py 4 5 7 24 102 pts/rs56 > ctl/rand_s56.log 2>&1
$PY randsets.py 4 6 7 16 103 pts/rt57 > ctl/rand_t57.log 2>&1
: > ctl/check_rand.log
for f in pts/rhx_*.json; do $PY owner_check.py $f ctl/hx_N2.cnf >> ctl/check_rand.log 2>&1; done
for f in pts/rs56_*.json; do $PY owner_check.py $f ctl/s56_N2.cnf >> ctl/check_rand.log 2>&1; done
for f in pts/rt57_*.json pts/etv757.json pts/etv756.json pts/etv747.json; do $PY owner_check.py $f ctl/t57_N2_v1.cnf >> ctl/check_rand.log 2>&1; done
$PY owner_check.py pts/etv656.json ctl/hx_N2.cnf >> ctl/check_rand.log 2>&1
echo done > ctl/DONE
