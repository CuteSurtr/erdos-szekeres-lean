#!/bin/sh
# usage: solve.sh CUBEDIR TLIMIT   (BASE0 + CUBEDIR/cube.units -> cube.cnf; CaDiCaL 2.1.3 text LRAT; writes solved)
# If CUBEDIR/noproof exists (statistics-only probes): no proof, and the cnf is deleted afterwards.
d=$1; T=$2
BASE=/home/jay/research/data/satopen-20261113/k9/BASE0.cnf
read -r p c nv ncl < $BASE
nu=$(wc -l < $d/cube.units)
{ echo "p cnf $nv $((ncl + nu))"; tail -n +2 $BASE; cat $d/cube.units; } > $d/cube.cnf
sha256sum $d/cube.cnf > $d/cnf.sha256
t0=$(date +%s)
if [ -f $d/noproof ]; then
  cadical -t $T $d/cube.cnf > $d/cadical.out 2>&1; ec=$?
  rm -f $d/cube.cnf
  echo "cadical exit $ec seconds $(( $(date +%s) - t0 )) limit $T noproof" > $d/solved
else
  cadical -t $T --lrat --binary=false $d/cube.cnf $d/proof.lrat > $d/cadical.out 2>&1; ec=$?
  echo "cadical exit $ec seconds $(( $(date +%s) - t0 )) limit $T" > $d/solved
fi
