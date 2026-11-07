#!/bin/sh
# P1 open items 6 and 15 (7 November 2026). Run from cloud/es7-2026-10-19/results:
#   sh WRITEUP/P1/checks-20261107/run.sh OUTDIR
# 1. The ES8SYM pipeline (section 1 and the line-module part of section 5 of ES8SYM/tools/run_all.sh, the same
#    commands) on the three sevenfold files of PRIMEFOLD/sets/k8 that are not in ES8SYM/sets.
# 2. PRIMEFOLD/check64/modules60 (otable.py, run_modules.py) on c7_64_own_s1000.
# Needs Python 3 (standard library only) and a C compiler; set CC or CFLAGS if needed (on some macOS installs:
# CFLAGS="-O2 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX26.sdk"). Takes a few seconds.
# Logs go to WRITEUP/P1/checks-20261107/logs, with OUTDIR written as <out>.
set -e
O=$1; T=ES8SYM/tools; X=ES8SYM/structure; L=WRITEUP/P1/checks-20261107/logs
CC=${CC:-cc}; CFLAGS=${CFLAGS:--O2}; PY="${PYTHON:-python3} -B"
mkdir -p "$O" "$L"
for p in cvx2 cvxcheck; do $CC $CFLAGS -o "$O/$p" $T/$p.c; done
for p in inv modules; do $CC $CFLAGS -o "$O/$p" $X/$p.c; done

for n in c7_64_own_s1000 m7_x2_G9s_centre p7_two_orbit_64; do
  F=PRIMEFOLD/sets/k8/$n.pts
  {
    echo "-- $n  m=7 centre=1"
    shasum -a 256 $F
    $PY $T/layer_order.py $F 7 "$O/$n.L.pts"
    $PY $T/verify_cfg.py --pts "$O/$n.L.pts" 7 1 8 "$O/$n"
    "$O/cvx2" "$O/$n" 8
    $PY $T/otab2txt.py "$O/$n" "$O/$n.orient"
    "$O/cvxcheck" "$O/$n.orient" 8
    $PY $T/crosscheck_decimal.py "$O/$n" 7
    echo "== order-type invariants and line-modules"
    $PY $X/orient.py zeta 7 $F "$O/$n.ot"
    "$O/inv" "$O/$n.ot"
    "$O/modules" "$O/$n.ot" | grep -v '^module '
  } 2>&1 | sed "s#$O#<out>#g" > $L/es8sym_$n.log
done

R=$(pwd)
(cd PRIMEFOLD/check64/modules60 &&
  $PY otable.py ../../sets/k8/c7_64_own_s1000.pts "$O/own.otv" &&
  $PY run_modules.py ../../sets/k8/c7_64_own_s1000.pts "$O/own.otv") 2>&1 | sed "s#$O#<out>#g" \
  > "$R/$L/modules60_c7_64_own_s1000.log"
echo done
