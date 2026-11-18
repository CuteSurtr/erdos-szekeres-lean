#!/bin/bash
# scaling in N for the 56-state catalog (CA=3, CB=5, G=7), no lemma rows: owner model with
# --sigmax 1 --link, "at least N occupied"; plain CaDiCaL 2.1.3, COMPUTED only, 900 s cap.
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
for N in 54 52 50 49 48 47 46 45; do
  $PY owner.py 3 5 7 $N exp/sc35_N$N.cnf --sigmax 1 --link > /dev/null 2>&1
  s=$(date +%s.%N); cadical -t 900 exp/sc35_N$N.cnf > exp/sc35_N$N.log 2>&1; e=$(date +%s.%N)
  r=$(grep -E '^s ' exp/sc35_N$N.log)
  echo "N=$N ${r:-s UNKNOWN} wall=$(echo "$e - $s" | bc) conflicts=$(grep -E '^c conflicts:' exp/sc35_N$N.log | awk '{print $3}')" >> exp/scale35.log
  rm -f exp/sc35_N$N.cnf
  if [ -z "$r" ]; then break; fi
done
echo done >> exp/scale35.log
