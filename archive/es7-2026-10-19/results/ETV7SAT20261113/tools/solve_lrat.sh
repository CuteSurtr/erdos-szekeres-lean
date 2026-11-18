#!/bin/bash
# usage: solve_lrat.sh name   (expects run/name.cnf) -> run/name.out, run/name.lrat, run/name.cake
# CaDiCaL 2.1.3 with a text LRAT proof, then cake_lpr; only "s VERIFIED UNSAT" certifies.
name=$1
t0=$(date +%s)
cadical --lrat --no-binary run/$name.cnf run/$name.lrat > run/$name.log 2>&1
ec=$?
t1=$(date +%s)
grep -E "^s " run/$name.log > run/$name.out
echo "exit=$ec cadical_wall=$((t1-t0))" >> run/$name.out
if [ $ec -eq 20 ]; then
  sha256sum run/$name.cnf run/$name.lrat > run/$name.cake
  ls -l run/$name.lrat | awk '{print "lrat_bytes="$5}' >> run/$name.cake
  ~/.local/bin/cake_lpr run/$name.cnf run/$name.lrat >> run/$name.cake 2>&1
  t2=$(date +%s)
  echo "cake_wall=$((t2-t1))" >> run/$name.cake
elif [ $ec -eq 10 ]; then
  grep -E "^v " run/$name.log > run/$name.model
fi
