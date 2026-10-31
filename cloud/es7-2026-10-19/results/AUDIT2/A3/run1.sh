#!/bin/bash
# usage: run1.sh name  -> solves /opt/work/ob/name.cnf, checks LRAT, prints json line
n=$1; c=/opt/work/ob/$n.cnf; p=/opt/work/ob/$n.lrat
s=$(date +%s.%N)
/opt/build/cadical/build/cadical -q --lrat=true --no-binary $c $p >/opt/work/ob/$n.out 2>&1; rc=$?
m=$(date +%s.%N)
v=$(/opt/build/cake_lpr/cake_lpr $c $p 2>&1 | grep -x 's VERIFIED UNSAT')
e=$(date +%s.%N)
sz=$(stat -c %s $p)
rm -f $p
echo "{\"obligation_file\":\"$n\",\"cnf_sha256\":\"$(sha256sum $c|cut -d' ' -f1)\",\"cadical_rc\":$rc,\"proof_bytes\":$sz,\"cake_lpr\":\"$v\",\"solve_s\":$(echo "$m-$s"|bc),\"check_s\":$(echo "$e-$m"|bc)}"
