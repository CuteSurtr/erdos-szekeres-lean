#!/bin/bash
# wrapper for cake_lpr a36874a (which reads heap/stack sizes only from --CML_* flags).
# 1st try: heap 5000 MB in one of two lock slots (two checks at once fit in 15 GB).
# If that does not print "s VERIFIED UNSAT", retry with the driver's CML_HEAP_SIZE/CML_STACK_SIZE
# holding both slots. Output is cake_lpr's own output of the last attempt.
B=/opt/build/cake_lpr/cake_lpr; L=/opt/work
ST=${CML_STACK_SIZE:+--CML_STACK_SIZE=$CML_STACK_SIZE}
run_small() { flock -n $L/cake0.lock $B --CML_HEAP_SIZE=5000 $ST "$@" && return 0; [ $? -ne 1 ] && return 0; flock $L/cake1.lock $B --CML_HEAP_SIZE=5000 $ST "$@"; }
out=$(run_small "$@" 2>&1)
if printf '%s\n' "$out" | head -1 | grep -qx "s VERIFIED UNSAT"; then printf '%s\n' "$out"; exit 0; fi
echo "$(date -u +%T) small-heap attempt not accepted on $*: $(printf '%s' "$out" | head -2 | tr '\n' ' ')" >> $L/cake_retries.log
exec flock $L/cake0.lock flock $L/cake1.lock $B ${CML_HEAP_SIZE:+--CML_HEAP_SIZE=$CML_HEAP_SIZE} $ST "$@"
