#!/bin/bash
# usage: runcad.sh NAME CNF LIMIT [cadical options] -> cad_NAME.out ; with --lrat writes NAME.lrat
D=$(cd "$(dirname "$0")" && pwd); B=$D/../local/bin; name=$1; f=$2; lim=$3; shift 3; cd $D
if [[ " $* " == *" --lrat "* ]]; then
  nohup $B/cadical -t $lim "$@" --binary=false $f $name.lrat > cad_$name.out 2>&1 &
else
  nohup $B/cadical -t $lim "$@" $f > cad_$name.out 2>&1 &
fi
echo "$name pid $!"
