#!/bin/bash
# Two-way random tests of zcnf.py (zrandtest.py): CNF + chirotope units SAT <=> largest convex subset < K.
cd "$(dirname "$0")"; mkdir -p rt
run() { local f=rt/$1; shift; python3 zcnf.py "$@" -o $f.cnf --map $f.json > /dev/null; }
for spec in "rot 2 6 6 --hull" "rot 2 7 6 --hull" "rot 2 6 5" "rot 4 3 6" "rot 4 4 6" "mirror 2 6 6" "mirror 2 7 6" "mirror 2 6 5" \
            "rot 2 5 7 --hull" "rot 2 6 7 --hull" "rot 2 6 7" "rot 4 3 7" "mirror 2 5 7" "mirror 2 6 7" "rot 2 7 7 --hull" "mirror 2 7 7"; do
  set -- $spec; n=${1}_m$2_t$3_k$4${5:+h}
  run $n $1 $3 $4 --m $2 $5
  python3 zrandtest.py $1 $2 $3 $4 rt/$n.cnf rt/$n.json 150 7 $5 | tail -1
done
for spec in "5 7 1" "6 7 1" "5 7 2" "6 7 2" "6 6 1" "5 6 2"; do
  set -- $spec; n=mirror_t$1_k$2_a$3
  run $n mirror $1 $2 --axis $3
  python3 zrandtest.py mirror 2 $1 $2 rt/$n.cnf rt/$n.json 150 5 --axis $3 | tail -1
done
