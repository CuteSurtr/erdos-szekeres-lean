#!/bin/bash
# (copy of <six10-work-dir>/realize/p2/mfold/tools/verify_mf.sh)
# verify_mf.sh PTS M C DIR : the ES8SYM exact pipeline (verify_cfg A+B, cvx2 two DPs, cvxcheck DFS+DP, crosscheck_decimal)
T=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ES8SYM/tools
mkdir -p $4; cp $1 $4/c_in.pts; cd $4
[ -x cvx2 ] || gcc -O2 -o cvx2 $T/cvx2.c; [ -x cvxcheck ] || gcc -O2 -o cvxcheck $T/cvxcheck.c
{ echo "== layer_order"; python3 -B $T/layer_order.py c_in.pts $2 c.L.pts; echo "rc=$?"
  echo "== verify_cfg"; python3 -B $T/verify_cfg.py --pts c.L.pts $2 $3 8 c; echo "rc=$?"
  echo "== cvx2"; ./cvx2 c 8; echo "rc=$?"
  echo "== cvxcheck"; python3 -B $T/otab2txt.py c c.orient; ./cvxcheck c.orient 8; echo "rc=$?"
  echo "== crosscheck_decimal"; python3 -B $T/crosscheck_decimal.py c $2; echo "rc=$?"; } > verify.log 2>&1
grep -E "PASS|FAIL|convex  8|8-subsets|largest|zero_orient|rc=" verify.log
