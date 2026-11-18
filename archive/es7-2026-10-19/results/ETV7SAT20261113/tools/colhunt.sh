#!/bin/bash
# colhunt.sh "N1 N2 ..." TLIM : search for 2-colourings of the triples of N ordered vertices with no
# 5-cap path and no weak heptagon (signotope-free owner model with rows, exactly N); a model is decoded
# and checked independently (pattern_of.py), then re-encoded semantically (owner_check.py --coloring).
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
for N in $1; do
  name=hunt_N$N
  $PY owner.py 3 5 7 $N om/$name.base.cnf --names --nosig > run/$name.gen.log 2>&1
  $PY addrows.py om/$name.base.cnf run/$name.cnf S1:25 S2:25 B1:16 B2:16 ALL:$N >> run/$name.gen.log 2>&1
  rm -f om/$name.base.cnf om/$name.base.cnf.names.pkl
  s=$(date +%s)
  cadical -t $2 run/$name.cnf > run/$name.log 2>&1
  ec=$?
  r="no verdict"
  if [ $ec -eq 10 ]; then
    grep -E "^v " run/$name.log > run/$name.model
    chk=$($PY pattern_of.py $name 2>&1 | tail -1)
    rt=$($PY owner_check.py run/$name.coloring.json run/$name.cnf --coloring 2>&1 | tail -1)
    r="SAT check=$chk roundtrip=$rt"
  elif [ $ec -eq 20 ]; then r="UNSAT (COMPUTED, no proof)"; fi
  echo "N=$N wall=$(( $(date +%s) - s )) conflicts=$(grep -E '^c conflicts:' run/$name.log | awk '{print $3}') $r" >> run/colhunt.log
  rm -f run/$name.cnf
done
echo done >> run/colhunt.log
