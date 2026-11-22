#!/bin/bash
# Rebuild the five ENCBLEAN modules in the printer/theorem closure (Gen, Dimacs, Coded, Cover, Render) from copies of
# their sources (ref/encb/EncB, sha256 = the ENCBLEAN record's files) and compare the IR C and oleans byte for byte
# with the ENCBLEAN .lake files used by link.sh and LEAN_PATH. Log: logs/encb_check.log
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
O=$D/build/encb_check
rm -rf $O; mkdir -p $O/olean/EncB $O/ir/EncB
export LEAN_PATH="$TC/lib/lean:$O/olean"
cd $D/ref/encb
for m in Gen Dimacs Coded Cover Render; do
  /usr/bin/time -f "EncB.$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . -o $O/olean/EncB/$m.olean \
    -i $O/olean/EncB/$m.ilean -c $O/ir/EncB/$m.c EncB/$m.lean || { echo "FAIL $m"; exit 1; }
done
for m in Gen Dimacs Coded Cover Render; do
  cmp -s $O/ir/EncB/$m.c $ENCB/.lake/build/ir/EncB/$m.c && echo "IR_IDENTICAL $m" || echo "IR_DIFFERS $m"
  cmp -s $O/olean/EncB/$m.olean $ENCB/.lake/build/lib/lean/EncB/$m.olean && echo "OLEAN_IDENTICAL $m" || echo "OLEAN_DIFFERS $m"
done
echo "ENCB_CHECK_DONE"
