#!/bin/sh
cd /home/jay/research/data/satopen-20261113/m9/root
t0=$(date +%s)
cadical -t 7400 --lrat --binary=false root.cnf root.lrat > cadical.out 2>&1; ec=$?
echo "cadical exit $ec seconds $(( $(date +%s) - t0 ))" > solved
