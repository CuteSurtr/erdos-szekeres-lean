#!/bin/bash
# vfy.sh NAME [HEAP_MB] : cake_lpr on run/NAME.cnf + run/NAME.lrat in its own transient unit
# nov13c-vfy-e7-NAME (memory policy of 18:25: verifiers have their own budget; bounded CakeML heap,
# MemorySwapMax=0).  Appends hashes and the cake_lpr output to run/NAME.cake.  Blocks until done.
name=$1; heap=${2:-2600}
mm=$(( heap + 200 + (heap + 200) / 4 ))
{ echo "vfy heap=${heap}MB $(date)"; sha256sum run/$name.cnf run/$name.lrat; ls -l run/$name.lrat | awk '{print "lrat_bytes="$5}'; } >> run/$name.cake
t1=$(date +%s)
u=nov13c-vfy-e7-$(echo $name | tr '_' '-' | tr 'A-Z' 'a-z')
systemd-run --user --wait --collect --quiet --unit=$u -p CPUQuota=100% -p MemoryMax=${mm}M -p MemorySwapMax=0 -p RuntimeMaxSec=2400 --nice=10 --working-directory=$PWD \
  bash -c "~/.local/bin/cake_lpr --CML_HEAP_SIZE=$heap --CML_STACK_SIZE=200 run/$name.cnf run/$name.lrat >> run/$name.cake 2>&1"
echo "vfy_exit=$? cake_wall=$(( $(date +%s) - t1 )) $(date)" >> run/$name.cake
