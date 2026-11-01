#!/bin/bash
# leaf.sh <i> <cube literals...>: build cubeCnf, solve, check, print one JSON line
set -u
i=$1; shift; lits=("$@")
T=/tmp/claude-0/tools; W=/tmp/claude-0/work; S=$W/leaf$i; mkdir -p $S
BODY=$W/body.cnf; NV=47002; NC=535454
n=${#lits[@]}
{ echo "p cnf $NV $((NC+n))"; cat $BODY; for l in "${lits[@]}"; do echo "$l 0"; done; } > $S/f.cnf
csha=$(sha256sum $S/f.cnf | cut -d' ' -f1)
t0=$(date +%s.%N)
$T/cadical/build/cadical -q --lrat=true --no-binary $S/f.cnf $S/p.lrat > $S/cad.out 2>&1; ex=$?
t1=$(date +%s.%N)
pb=$(stat -c %s $S/p.lrat 2>/dev/null || echo 0)
psha=$(sha256sum $S/p.lrat 2>/dev/null | cut -d' ' -f1)
$T/cake_lpr/cake_lpr $S/f.cnf $S/p.lrat > $S/cake.out 2>&1; cex=$?
t2=$(date +%s.%N)
if grep -qx 's VERIFIED UNSAT' $S/cake.out; then cl='s VERIFIED UNSAT'; else cl="$(tail -c 300 $S/cake.out) [exit $cex]"; fi
python3 -c '
import json,sys
a=sys.argv
print(json.dumps({"i":int(a[1]),"cube":[int(x) for x in a[2].split()],"cnf_sha256":a[3],"solver_exit":int(a[4]),"solve_s":round(float(a[5]),2),"proof_bytes":int(a[6]),"proof_sha256":a[7],"cake_lpr":a[8],"check_s":round(float(a[9]),2)}))
' "$i" "${lits[*]}" "$csha" "$ex" "$(echo "$t1-$t0"|bc)" "$pb" "$psha" "$cl" "$(echo "$t2-$t1"|bc)"
rm -rf $S
