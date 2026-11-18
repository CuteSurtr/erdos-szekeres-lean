#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
$PY owner.py 3 4 7 2 ctl/s56_N2_nosig.cnf --names --nosig > /dev/null
$PY colcontrol.py 3 4 7 ctl/s56_N2_nosig.cnf 14,16,18,20,22,24,25 1,2,3 > ctl/colcontrol_347.log 2>&1
$PY owner.py 3 5 7 2 ctl/t57_N2_nosig.cnf --names --nosig > /dev/null
$PY colcontrol.py 3 5 7 ctl/t57_N2_nosig.cnf 16,20,24,26 1,2 > ctl/colcontrol_357.log 2>&1
rm -f ctl/t57_N2_nosig.cnf ctl/t57_N2_nosig.cnf.names.pkl
echo done >> ctl/colcontrol_357.log
