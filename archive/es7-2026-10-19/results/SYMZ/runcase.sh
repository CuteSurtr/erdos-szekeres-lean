#!/bin/bash
# usage: runcase.sh CASEDIR NAME LIMIT [cadical options]: base CNF (CASEDIR/base path in CASEDIR/BASE) + the cube NAME
# from CASEDIR/cubes.txt -> CASEDIR/NAME.cnf, cad output CASEDIR/NAME.out (and NAME.lrat with --lrat)
D=$(cd "$(dirname "$0")" && pwd); B=$D/../local/bin; dir=$1; name=$2; lim=$3; shift 3
base=$(cat $dir/BASE); f=$dir/$name.cnf
lits=$(grep "^$name " $dir/cubes.txt | cut -d' ' -f2-)
n=$(echo $lits | wc -w | tr -d ' ')
awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $base > $f
for l in $lits; do echo "$l 0"; done >> $f
if [[ " $* " == *" --lrat "* ]]; then
  $B/cadical -t $lim "$@" --binary=false $f $dir/$name.lrat > $dir/$name.out 2>&1
else
  $B/cadical -t $lim "$@" $f > $dir/$name.out 2>&1
fi
rm -f $f
