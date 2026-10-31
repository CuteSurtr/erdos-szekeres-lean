#!/bin/bash
# usage: check.sh NAME CNFBASE CHECKER  -> chk_NAME_CHECKER.out with wall time
D=$(cd "$(dirname "$0")" && pwd); B=$D/../../local/bin; cd $D
export CML_HEAP_SIZE=${CML_HEAP_SIZE:-12000} CML_STACK_SIZE=2000
s=$(date +%s); /usr/bin/time -l $B/$3 $2.cnf $1.lrat > chk_$1_$3.out 2>&1; echo "exit $? wall $(( $(date +%s) - s )) s" >> chk_$1_$3.out
