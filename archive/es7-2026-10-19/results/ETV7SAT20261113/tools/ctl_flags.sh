#!/bin/bash
# ctl_flags.sh TAG "GENERATOR FLAGS": positive control of a generator variant on the 26-point ETV
# set and its mirror image (with rows and ALL:26), and on four random sets (N=2, rows).
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
tag=$1; flags=$2
$PY owner.py 3 5 7 26 ctl/f_$tag.base.cnf --names $flags > ctl/f_$tag.gen.log 2>&1
$PY addrows.py ctl/f_$tag.base.cnf ctl/f_$tag.cnf S1:25 S2:25 B1:16 B2:16 ALL:26 >> ctl/f_$tag.gen.log 2>&1
$PY owner_check.py pts/etv757.json ctl/f_$tag.cnf > ctl/check_f_$tag.log 2>&1
$PY owner_check.py pts/etv757.json ctl/f_$tag.cnf --mirror >> ctl/check_f_$tag.log 2>&1
$PY owner.py 3 5 7 2 ctl/f_$tag.base.cnf --names $flags >> ctl/f_$tag.gen.log 2>&1
$PY addrows.py ctl/f_$tag.base.cnf ctl/f_$tag.cnf S1:25 S2:25 B1:16 B2:16 >> ctl/f_$tag.gen.log 2>&1
for i in 0 5 10 15; do $PY owner_check.py pts/rt57_$i.json ctl/f_$tag.cnf >> ctl/check_f_$tag.log 2>&1; done
rm -f ctl/f_$tag.base.cnf* ctl/f_$tag.cnf*
echo done >> ctl/check_f_$tag.log
