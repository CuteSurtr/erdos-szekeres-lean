#!/bin/bash
# usage: chk.sh CNF PROOF TAG -> chk_TAG_lrat-check.out, chk_TAG_cake_lpr.out (both in background; heap via flag)
D=$(cd "$(dirname "$0")" && pwd); B=$D/../local/bin; cd $D
( s=$(date +%s); /usr/bin/time -l $B/lrat-check $1 $2 > chk_$3_lrat-check.out 2>&1; echo "exit $? wall $(( $(date +%s) - s )) s" >> chk_$3_lrat-check.out ) &
( s=$(date +%s); /usr/bin/time -l $B/cake_lpr --CML_HEAP_SIZE=30000 --CML_STACK_SIZE=4000 $1 $2 > chk_$3_cake_lpr.out 2>&1; echo "exit $? wall $(( $(date +%s) - s )) s" >> chk_$3_cake_lpr.out ) &
wait
