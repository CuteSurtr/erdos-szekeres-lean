#!/bin/bash
# usage: launch.sh NAME CNFBASE [cadical options...]; writes cad_NAME.out (and NAME.lrat with --lrat)
D=$(cd "$(dirname "$0")" && pwd); B=$D/../../local/bin; name=$1; f=$2; shift 2
cd $D
if [[ " $* " == *" --lrat "* ]]; then
  nohup $B/cadical -t 7200 "$@" --binary=false $f.cnf $name.lrat > cad_$name.out 2>&1 &
else
  nohup $B/cadical -t 7200 "$@" $f.cnf > cad_$name.out 2>&1 &
fi
echo "$name pid $! : cadical -t 7200 $* $f.cnf"
