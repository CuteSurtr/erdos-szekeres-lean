#!/bin/bash
# Direct E1+E2 spot check: cake_lpr (heap 600 MB) on the exact text `ae33print cnf i` writes, with L18's kept LRAT
# for that pair; count the exact line `s VERIFIED UNSAT` (cake_lpr exits 0 even on rejection). Negative control:
# the LRAT of the first pair against the CNF of the second must give 0 verdict lines. Temporary files deleted.
D=/home/jay/research/data/formalize-20261122/ae33-lean
X=$D/build/bin/ae33print
E=/home/jay/research/data/roadmap-20261115/pm1115/l1118/e72
T=$D/tmp; mkdir -p $T
first=""
for i in "$@"; do
  nm=$($X name $i)
  $X cnf $i > $T/$i.cnf
  zstd -q -dc $E/cert/$nm.lrat.zst > $T/$i.lrat
  out=$(/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=600 $T/$i.cnf $T/$i.lrat 2>&1)
  echo "spot $i $nm cnf_sha=$(sha256sum $T/$i.cnf | cut -c1-16) verdict_lines=$(grep -cx 's VERIFIED UNSAT' <<< "$out") lines=$(wc -l <<< "$out")"
  if [ -z "$first" ]; then first=$i; else
    neg=$(/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=600 $T/$i.cnf $T/$first.lrat 2>&1)
    echo "negctl lrat($first) vs cnf($i): verdict_lines=$(grep -cx 's VERIFIED UNSAT' <<< "$neg") first_line=$(head -1 <<< "$neg" | cut -c1-80)"
    rm -f $T/$first.cnf $T/$first.lrat; first=$i
  fi
done
rm -rf $T
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "cgroup memory.peak=$(( $(cat $CG/memory.peak 2>/dev/null || echo 0) / 1048576 )) MB"
