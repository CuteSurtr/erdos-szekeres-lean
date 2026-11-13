#!/bin/sh
# two single-threaded m9cc.py drivers in one unit (CPUQuota 200 %): main tree cc1 and the delegated subtree r10 -> cc2
cd /home/jay/research/data/satopen-20261113/m9
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
OUT=/home/jay/research/data/satopen-20261113/m9/cc1 TL=2 PL=600 CAKEHEAP=800 $PY -u tools/m9cc.py > cc1.driver.out 2>&1 &
OUT=/home/jay/research/data/satopen-20261113/m9/cc2 ROOT='[-11834, -11899, 11783]' TL=2 PL=600 CAKEHEAP=800 $PY -u tools/m9cc.py > cc2.driver.out 2>&1 &
wait
