#!/bin/sh
# launch.sh SECONDS RUN... : start one CaDiCaL lane per run name (RUN.cnf), no proof output, with the RULES.md RAM check.
D="<repo>/.cache/es7/final-2026-11-04/five_identities"
C="<repo>/.cache/es7/bin/cadical"
cd "$D" || exit 1
T=$1; shift
for r in "$@"; do
  R=$(vm_stat | awk '/Pages active/{a=$3}/wired down/{w=$4}/occupied by compressor/{c=$5}END{printf "%.1f\n",(a+w+c)*16384/1e9}')
  echo "$(date +%T) RAM $R start $r t=$T" >> logs/launch.txt
  awk -v r="$R" 'BEGIN{exit !(r<40)}' || { echo "$(date +%T) RAM too high, $r not started" >> logs/launch.txt; continue; }
  nohup /usr/bin/time -l "$C" -t "$T" --no-binary "$r.cnf" > "logs/$r.log" 2> "logs/$r.time" &
  sleep 1
done
