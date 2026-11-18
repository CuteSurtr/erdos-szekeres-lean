#!/bin/bash
# watch_finish.sh TAG N "FLAGS" OLDUNIT [HEAP]: wait for CaDiCaL of run/lad_TAG_N$N to end (its wrapper
# is frozen so that it cannot start cake_lpr with the default 4 GB heap), then verify via vfy.sh, log,
# and stop the old unit.
tag=$1; N=$2; flags=$3; unit=$4; heap=${5:-2600}
name=lad_${tag}_N$N
until grep -q "^c exit" run/$name.log 2>/dev/null; do sleep 5; done
sleep 2
ec=$(grep -E "^c exit" run/$name.log | awk '{print $3}')
if [ "$ec" != "20" ]; then rm -f run/$name.lrat; fi
./finish_run.sh $tag $N "$flags" $heap
systemctl --user stop $unit
