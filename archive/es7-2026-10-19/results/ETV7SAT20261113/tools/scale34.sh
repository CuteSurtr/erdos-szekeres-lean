#!/bin/bash
# scaling in N for the 35-state catalog (CA=3, CB=4, G=7): owner model, at least N occupied
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
for N in 34 32 30 28 27; do
  $PY owner.py 3 4 7 $N exp/sc34_N$N.cnf > /dev/null 2>&1
  s=$(date +%s.%N); cadical exp/sc34_N$N.cnf > exp/sc34_N$N.log 2>&1; e=$(date +%s.%N)
  echo "N=$N $(grep -E '^s ' exp/sc34_N$N.log) wall=$(echo "$e - $s" | bc) conflicts=$(grep -E '^c conflicts:' exp/sc34_N$N.log | awk '{print $3}')" >> exp/scale34.log
  rm -f exp/sc34_N$N.cnf
done
echo done >> exp/scale34.log
