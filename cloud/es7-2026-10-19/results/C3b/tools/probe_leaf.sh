#!/bin/bash
# usage: probe_leaf.sh CNF CUBES INDEX TLIM OUTJSONL  -- plain CaDiCaL (no proof) on CNF + cube units
CAD=${CAD:-/tmp/claude-0/build/cadical/build/cadical}; W=${W:-/tmp/claude-0/cncwork}; mkdir -p $W
lits=$(grep "^a " $2 | sed -n "$(( $3 + 1 ))p" | sed 's/^a //; s/ 0$//')
n=$(echo $lits | wc -w); f=$W/probe$3.cnf
awk -v n=$n 'NR==FNR && /^p cnf/ {print "p cnf", $3, $4+n; next} {print}' $1 > $f
for l in $lits; do echo "$l 0" >> $f; done
t0=$(date +%s); st=$($CAD -t $4 $f | tee $W/probe$3.log | grep "^s " | cut -c3-); t1=$(date +%s)
conf=$(grep "^c conflicts:" $W/probe$3.log | awk '{print $3}')
echo "{\"cube\":$3,\"lits\":\"$lits\",\"status\":\"${st:-UNKNOWN}\",\"wall_s\":$((t1-t0)),\"conflicts\":${conf:-0},\"tlim\":$4}" >> $5
[ "$st" = "SATISFIABLE" ] && cp $W/probe$3.log $5.model$3
rm -f $f
