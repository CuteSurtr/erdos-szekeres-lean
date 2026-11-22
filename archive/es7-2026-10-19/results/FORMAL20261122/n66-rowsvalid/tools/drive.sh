#!/bin/bash
# Compile modules one lean process each, in order; stop at the first failure. usage: drive.sh Mod1 Mod2 ...
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
for m in "$@"; do
  $D/tools/lc.sh $m > /dev/null
  r=$(grep -E '^rc=' $D/logs/$(echo $m | tr / _).log | tail -1)
  echo "$(date '+%T') $m $r $(grep Elapsed $D/logs/$(echo $m | tr / _).log | awk '{print $NF}') $(grep 'Maximum resident' $D/logs/$(echo $m | tr / _).log | awk '{print $NF}')" >> $D/logs/drive.log
  [ "$r" = "rc=0" ] || exit 1
done
