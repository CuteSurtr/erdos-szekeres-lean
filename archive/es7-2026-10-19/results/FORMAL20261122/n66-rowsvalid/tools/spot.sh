#!/bin/bash
# Spot check: print a few certificates and compare SHA-256 with VB's recorded cnf_sha256 (manifest).
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
for spec in "$@"; do
  k=${spec%:*}; i=${spec#*:}
  want=$(awk -F'\t' -v k=$k -v i=$i 'NR>1 && $2==k && $1==i {print $5}' $D/data/certs_manifest.tsv)
  kk=$(echo $k | tr TC tc)
  got=$( { /usr/bin/time -f "%e s %M KB" $D/build/bin/rowprint $kk $i | sha256sum | cut -c1-64; } 2> $D/logs/spot_time_$k$i.txt )
  echo "$k $i want=$want got=$got $( [ "$want" = "$got" ] && echo MATCH || echo MISMATCH ) $(cat $D/logs/spot_time_$k$i.txt)"
done
