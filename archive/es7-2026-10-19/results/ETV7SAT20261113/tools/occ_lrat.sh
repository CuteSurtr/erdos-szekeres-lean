#!/bin/bash
# usage: occ_lrat.sh name cnfname prio tlimit [opts]  -> run/name.{log,out,lrat,cake}
# drv/occfirst (CaDiCaL 3.0.1 library, decision priority on the listed literals) with a text LRAT
# proof of run/cnfname.cnf, then cake_lpr.  Only "s VERIFIED UNSAT" certifies.
name=$1; cnf=$2; prio=$3; tl=$4; shift; shift; shift; shift
t0=$(date +%s)
drv/occfirst run/$cnf.cnf $prio run/$name.lrat $tl "$@" > run/$name.log 2>&1
ec=$?
t1=$(date +%s)
grep -E "^s " run/$name.log > run/$name.out
echo "exit=$ec solver_wall=$((t1-t0)) $(date)" >> run/$name.out
if [ $ec -eq 20 ]; then
  sha256sum run/$cnf.cnf run/$name.lrat > run/$name.cake
  ls -l run/$name.lrat | awk '{print "lrat_bytes="$5}' >> run/$name.cake
  ~/.local/bin/cake_lpr run/$cnf.cnf run/$name.lrat >> run/$name.cake 2>&1
  t2=$(date +%s)
  echo "cake_wall=$((t2-t1)) $(date)" >> run/$name.cake
elif [ $ec -eq 10 ]; then
  grep -E "^v " run/$name.log > run/$name.model
else
  rm -f run/$name.lrat
fi
