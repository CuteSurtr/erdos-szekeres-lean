#!/bin/bash
# integer optimum of residual holes for capacities c = 56..50 (HiGHS B&B, 5 min each max)
for c in 56 55 54 53 52; do
  timeout 400 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u cap_mip.py $c 330 > cap_mip$c.log 2>&1
  tail -1 cap_mip$c.log
done
