#!/bin/bash
# recheck.sh NAME : (re)run cake_lpr on run/NAME.cnf + run/NAME.lrat, append to run/NAME.cake
name=$1
t1=$(date +%s)
echo "recheck $(date)" >> run/$name.cake
sha256sum run/$name.cnf run/$name.lrat >> run/$name.cake
~/.local/bin/cake_lpr run/$name.cnf run/$name.lrat >> run/$name.cake 2>&1
echo "exit=$? cake_wall=$(( $(date +%s) - t1 )) $(date)" >> run/$name.cake
