#!/bin/bash
# Real-set tests of zcnf.py: each real symmetric set, labelled in the normal form, satisfies the CNF with its chirotope
# fixed (SAT); a deliberately wrong labelling is rejected (UNSAT). R = results directory of the repository.
cd "$(dirname "$0")"; R=$1; B=${CADICAL:-cadical}
gen() { [ -f val/$1.cnf ] || python3 zcnf.py "${@:2}" -o val/$1.cnf --map val/$1.json > /dev/null; }
mkdir -p val
gen r2_t16k7h rot 16 7 --m 2 --hull; gen r2_t8k6h rot 8 6 --m 2 --hull; gen r2_t14k7h rot 14 7 --m 2 --hull
gen r4_t7k7 rot 7 7 --m 4; gen r4_t4k6 rot 4 6 --m 4; gen m_t16k7 mirror 16 7; gen m_t5k6a2 mirror 5 6 --axis 2
while read kind m pts cnf opts; do
  for sw in "" --swap; do
    o2=$opts; [ -n "$sw" ] && o2="$opts --swap"
    msg=$(python3 zvalidate.py $kind $m $R/$pts val/$cnf.json val/u.txt $o2 | tail -1)
    ./with_units.sh val/$cnf.cnf val/u.txt val/t.cnf
    echo "$pts on $cnf ${o2:-(normal form)}: $($B -q -t 600 val/t.cnf | grep '^s ') | $msg"
  done
  if [ "$opts" = "--hull" ]; then
    python3 zvalidate.py $kind $m $R/$pts val/$cnf.json val/u.txt --nothull > /dev/null
    ./with_units.sh val/$cnf.cnf val/u.txt val/t.cnf
    echo "$pts on $cnf --nothull (deliberately wrong): $($B -q -t 600 val/t.cnf | grep '^s ')"
  fi
done <<'LIST'
rot 2 SYM2/sym7_32points.txt r2_t16k7h --hull
rot 2 SYMMAX/k6/c2_16points.txt r2_t8k6h --hull
rot 2 SYMMAX/k6/c4_16points.txt r2_t8k6h --hull
rot 2 SYMMAX/c4_28points.txt r2_t14k7h --hull
rot 4 SYMMAX/c4_28points.txt r4_t7k7
rot 4 SYMMAX/k6/c4_16points.txt r4_t4k6
mirror 2 SYMMAX/mirror_32points.txt m_t16k7
mirror 2 SYMMAX/k6/mirror_12points.txt m_t5k6a2
LIST
rm -f val/t.cnf val/u.txt
